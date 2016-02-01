#!/usr/bin/make -f

SPECTOOL=$(shell which spectool)

.PHONY: all

all: fetch_sources build_srpms build_rpms

fetch_sources:
	$(SPECTOOL) -g -S -C sources/ specs/aacplusenc.spec
	$(SPECTOOL) -g -S -C sources/ specs/lame.spec
	$(SPECTOOL) -g -S -C sources/ specs/libdvdcss.spec
	$(SPECTOOL) -g -S -C sources/ specs/libfdk-aac.spec
	$(SPECTOOL) -g -S -C sources/ specs/libvo-aacenc.spec
	$(SPECTOOL) -g -S -C sources/ specs/libvo-amrwbenc.spec
	$(SPECTOOL) -g -S -C sources/ specs/libxvidcore.spec

build_srpms:
	mock --buildsrpm --spec specs/aacplusenc.spec --sources sources/ --resultdir build/source
	mock --buildsrpm --spec specs/lame.spec --sources sources/ --resultdir build/source
	mock --buildsrpm --spec specs/libdvdcss.spec --sources sources/ --resultdir build/source
	mock --buildsrpm --spec specs/libfdk-aac.spec --sources sources/ --resultdir build/source
	mock --buildsrpm --spec specs/libvo-aacenc.spec --sources sources/ --resultdir build/source
	mock --buildsrpm --spec specs/libvo-amrwbenc.spec --sources sources/ --resultdir build/source
	mock --buildsrpm --spec specs/libxvidcore.spec --sources sources/ --resultdir build/source

build_rpms:
	# build i686 RPMS
	mockchain -r fedora-23-i386 -l build --recurse build/source/*.src.rpm
	# build x86_64 RPMS
	mockchain -r fedora-23-x86_64 -l build --recurse build/source/*.src.rpm

clean:
	find build -mindepth 1 -maxdepth 1 -not -iname '.gitignore' -exec rm -fr {} \;
	find sources -mindepth 1 -maxdepth 1 -not \( -iname '*.patch' -or -iname '.gitignore' \) -exec rm -fr {} \;
