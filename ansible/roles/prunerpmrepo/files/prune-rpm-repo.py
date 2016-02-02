#!/usr/bin/python -tt

# Copyright 2014 Eucalyptus Systems, Inc.
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from __future__ import print_function

import datetime
import logging
import operator
import optparse
import os.path
import re
import sys

import rpm
import rpmUtils.miscutils
import yaml


class PackageInfo(object):
    # We're only using a class here because sorted loses its cmp arg in
    # python 3, and we actually do need a comparison function -- the
    # key arg is not sufficient.
    def __init__(self, name, epoch, version, release, arch,
                 is_sourcepackage=None, filename=None):
        self.name = name
        self.epoch = epoch or 0
        self.version = version
        self.release = release
        self.arch = arch
        self.is_sourcepackage = is_sourcepackage
        self.filename = filename

    @classmethod
    def from_file(cls, filename):
        ts = rpm.TransactionSet()
        ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
        with open(filename) as pkg:
            headers = ts.hdrFromFdno(pkg.fileno())
        if headers['sourcepackage']:
            arch = 'src'
        else:
            arch = headers['arch']
        return cls(headers['name'], headers['epoch'], headers['version'],
                   headers['release'], arch, headers['sourcepackage'],
                   filename=filename)

    @property
    def evr(self):
        return (self.epoch, self.version, self.release)

    @property
    def mtime(self):
        return os.path.getmtime(self.filename)

    # Note that this ignores Obsoletes and differences in package names.
    def __lt__(self, other):
        return rpmUtils.miscutils.compareEVR(self.evr, other.evr) < 0

    def __gt__(self, other):
        return rpmUtils.miscutils.compareEVR(self.evr, other.evr) > 0

    def __eq__(self, other):
        return rpmUtils.miscutils.compareEVR(self.evr, other.evr) == 0

    def __le__(self, other):
        return rpmUtils.miscutils.compareEVR(self.evr, other.evr) <= 0

    def __ge__(self, other):
        return rpmUtils.miscutils.compareEVR(self.evr, other.evr) >= 0

    def __ne__(self, other):
        return rpmUtils.miscutils.compareEVR(self.evr, other.evr) != 0

    def __repr__(self):
        #if self.epoch:
        #    fmt = '{name}-{epoch}:{version}-{release}.{arch}'
        #else:
        #    fmt = '{name}-{version}-{release}.{arch}'
        fmt = '{name}-{version}-{release}.{arch}'
        return fmt.format(**self.__dict__)


class Filter(object):
    def __init__(self, params):
        self.pattern = re.compile(params['pattern'])
        self.params = params

    def matches_pattern(self, package):
        return bool(self.pattern.match(str(package)))

    def get_pattern_matches(self, packages):
        return set(filter(self.matches_pattern, packages))

    def get_full_matches(self, packages):
        matching = self.get_pattern_matches(packages)
        filtered = set()
        if self.params.get('min-versions'):
            assert int(self.params['min-versions'])
            matched_by_rule = []
            preserved_versions = set()
            for package in sorted(matching, reverse=True):
                # This code *and* PackageInfo's comparisons do not
                # consider names, so be wary of running this loop on
                # multiple package names at once.
                if package.evr not in preserved_versions:
                    preserved_versions.add(package.evr)
                if len(preserved_versions) > self.params['min-versions']:
                    break
                matched_by_rule.append(package)
            for package in matched_by_rule:
                logging.debug("preserving %s (pattern = '%s', min-versions "
                              "= %i)", package, self.pattern.pattern,
                              self.params['min-versions'])
            filtered.update(matched_by_rule)
        if self.params.get('min-days'):
            assert int(self.params['min-days'])
            now = int(datetime.datetime.now().strftime('%s'))  # epoch time
            cutoff = now - self.params['min-days'] * 84600  # seconds per day
            matched_by_rule = sorted((match for match in matching
                                      if match.mtime > cutoff),
                                     key=operator.attrgetter('mtime'))
            for package in matched_by_rule:
                logging.debug("preserving %s (pattern = '%s', min-days "
                              "= %i)", package, self.pattern.pattern,
                              self.params['min-days'])
            filtered.update(matched_by_rule)
        return filtered


def find_old_packages(dirnames, filters=None):
    src_packages_by_name = {}
    bin_packages_by_name = {}
    for dirname in dirnames:
        for root, dirs, files in os.walk(dirname):
            for filename in files:
                path = os.path.join(root, filename)
                if os.path.isfile(path) and path.endswith('.rpm'):
                    try:
                        package = PackageInfo.from_file(path)
                    except rpm.error as err:
                        if err.args[0] == 'error reading package header':
                            logging.warn(
                                'file does not appear to be an rpm: %s',
                                path)
                        else:
                            raise
                    bin_packages_by_name.setdefault(package.name, set())
                    src_packages_by_name.setdefault(package.name, set())
                    if package.is_sourcepackage:
                        src_packages_by_name[package.name].add(package)
                    else:
                        bin_packages_by_name[package.name].add(package)

    old_packages = set()
    for package_map in (src_packages_by_name, bin_packages_by_name):
        for package_name in sorted(package_map):
            for filter in filters:
                applicable = filter.get_pattern_matches(
                    package_map[package_name])
                package_map[package_name] -= applicable
                preserved = filter.get_full_matches(applicable)
                old_packages.update(applicable - preserved)
    return old_packages


def read_filters(config_filename):
    with open(config_filename) as config_file:
        config = yaml.load(config_file)
    filters = []
    for filter_params in config.get('preserve') or []:
        filters.append(Filter(filter_params))
    return filters


def main():
    parser = optparse.OptionParser(
        description='Prune old packages from an rpm repository',
        usage='%prog [-nv] [--config FILE] [--debug] DIR ...')
    parser.add_option('--config', metavar='FILE',
                      help='configuration file')
    parser.add_option('-n', '--pretend', action='store_true',
                      help="don't actually remove packages.  Implies -v."),
    parser.add_option('-v', '--verbose', action='store_true',
                      help='list the files that are deleted'),
    parser.add_option('--debug', action='store_true', help='show '
                      'retention policy matches and other debugging info')
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_usage()
        sys.exit(1)
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)
    if options.config:
        filters = read_filters(options.config)
    else:
        filters = []
    if not any(filter.pattern == '.*' for filter in filters):
        filters.append(Filter({'pattern': '.*', 'max-versions': 1000000,
                               'max-days': 10000}))
    packages = find_old_packages(args, filters=filters)
    for package in sorted(packages, key=operator.attrgetter('filename')):
        if options.verbose or options.pretend:
            print('deleting', package.filename)
        if not options.pretend:
            os.remove(package.filename)


if __name__ == '__main__':
    main()
