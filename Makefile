#!/usr/bin/make -f

.PHONY: all

all: fetch_sources build_srpms build_rpms

fetch_sources:
	spectool -g -S -C sources/ specs/aacplusenc.spec
	spectool -g -S -C sources/ specs/ffmpeg.spec
	spectool -g -S -C sources/ specs/handbrake.spec
	spectool -g -S -C sources/ specs/lame.spec
	spectool -g -S -C sources/ specs/libdvdcss.spec
	spectool -g -S -C sources/ specs/libfdk-aac.spec
	spectool -g -S -C sources/ specs/libmfx.spec
	spectool -g -S -C sources/ specs/libvo-aacenc.spec
	spectool -g -S -C sources/ specs/libvo-amrwbenc.spec
	spectool -g -S -C sources/ specs/libxvidcore.spec
	spectool -g -S -C sources/ specs/makemkv.spec
	spectool -g -S -C sources/ specs/x264.spec
	spectool -g -S -C sources/ specs/x265.spec

build_srpms:
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/aacplusenc.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/ffmpeg.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/lame.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/handbrake.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/libdvdcss.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/libfdk-aac.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/libmfx.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/libvo-aacenc.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/libvo-amrwbenc.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/libxvidcore.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/makemkv.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/x264.spec
	mock -q --buildsrpm --sources sources/ --resultdir build/source --spec specs/x265.spec

build_rpms:
	# build i686 RPMS
	mockchain -r fedora-23-i386 -l build --recurse build/source/*.src.rpm
	# build x86_64 RPMS
	mockchain -r fedora-23-x86_64 -l build --recurse build/source/*.src.rpm

prune_repo:
	prune-rpm-repo -v --config prune-repo.yml build/results/

clean_build:
	find build -mindepth 1 -maxdepth 1 -not -iname '.gitignore' -exec rm -fr {} \;

clean_download:
	find sources -mindepth 1 -maxdepth 1 -not \( -iname '*.patch' -or -iname '.gitignore' \) -exec rm -fr {} \;

clean: clean_build clean_download
