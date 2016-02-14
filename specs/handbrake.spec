%global _hardened_build 1

%define package_name handbrake
%define package_version 1.0.0
%define package_release 2
%define package_git_long b63b0bb81471ca6d8aa89fc3800126dfe91d84bc
%define package_git_short %(c=%{package_git_long}; echo ${c:0:7})

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}.%{package_git_short}%{?dist}
Summary: HandBrake is a tool for converting video from nearly any format to a selection of modern, widely supported codecs.
License: GPLv2
URL: https://handbrake.fr
Source: https://github.com/HandBrake/HandBrake/archive/%{package_git_long}.tar.gz#/HandBrake-%{package_git_short}.tar.gz
Patch0: handbrake-patch-0001-qsv.patch

Conflicts: handbrake-legacy
Requires: libdvdcss%{_isa}

BuildRequires: bzip2-devel
BuildRequires: ffmpeg-devel
BuildRequires: liba52-devel
BuildRequires: libx265-devel >= 1.9-1
BuildRequires: libx264-devel
BuildRequires: libmpeg2-devel
BuildRequires: cmake
BuildRequires: bzip2-devel
BuildRequires: dbus-glib-devel
BuildRequires: desktop-file-utils
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: fribidi-devel
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: intltool
BuildRequires: jansson-devel
BuildRequires: libmp3lame-devel
BuildRequires: libappindicator-gtk3-devel
BuildRequires: libass-devel
BuildRequires: libbluray-devel >= 0.2.3
BuildRequires: libdvdnav-devel >= 5.0.1
BuildRequires: libdvdread-devel >= 5.0.0
BuildRequires: libfdk-aac-devel >= 0.1.4
BuildRequires: libgudev1-devel
BuildRequires: libmfx-devel
BuildRequires: libnotify-devel
BuildRequires: libogg-devel
BuildRequires: librsvg2-devel
BuildRequires: libsamplerate-devel
BuildRequires: libtheora-devel
BuildRequires: libtool
BuildRequires: libvorbis-devel
BuildRequires: libvpx-devel
BuildRequires: libxml2-devel
BuildRequires: m4
BuildRequires: make
BuildRequires: patch
BuildRequires: python
BuildRequires: subversion
BuildRequires: tar
BuildRequires: webkitgtk3-devel
BuildRequires: wget
BuildRequires: yasm
BuildRequires: zlib-devel
BuildRequires: checksec

%description
HandBrake is a tool for converting video from nearly any format to a selection of modern, widely supported codecs.

%prep -q

%setup -q -n HandBrake-%{package_git_long}
%patch0 -p1

%build
%ifarch %{ix86}
%define arch_bits 32
%else
%define arch_bits 64
%endif

CFLAGS="${CFLAGS:--O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m%{arch_bits} -mtune=generic}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:--O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m%{arch_bits} -mtune=generic}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:--O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m%{arch_bits} -mtune=generic -I/usr/lib64/gfortran/modules}" ; export FFLAGS ;
FCFLAGS="${FCFLAGS:--O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m%{arch_bits} -mtune=generic -I/usr/lib64/gfortran/modules}" ; export FCFLAGS ;
LDFLAGS="${LDFLAGS:--Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld}"; export LDFLAGS;
[ "1" = 1 ] && for i in $(find $(dirname ./configure) -name config.guess -o -name config.sub) ; do
  [ -f /usr/lib/rpm/redhat/$(basename $i) ] && /usr/bin/rm -f $i && /usr/bin/cp -fv /usr/lib/rpm/redhat/$(basename $i) $i ;
done ;
[ "1" = 1 ] && [ x != "x-specs=/usr/lib/rpm/redhat/redhat-hardened-ld" ] &&
  find . -name ltmain.sh | while read i ; do
    /usr/bin/sed -i.backup -e 's~compiler_flags=$~compiler_flags="-specs=/usr/lib/rpm/redhat/redhat-hardened-ld"~' $i
  done ;

for module in a52dec ffmpeg fdk-aac libdvdnav libdvdread libbluray libmfx libvpx x265 x264; do
  sed -i -e "/MODULES += contrib\/$module/d" make/include/main.defs
done

echo "GCC.args.O.speed = %{optflags} -lavcodec -lavdevice -lavfilter -lavformat -lavresample -lavutil -lpostproc -lswresample -lswscale -lx265 -lx264 -lfdk-aac -lmfx" > custom.defs
echo "GCC.args.g.none = " >> custom.defs

cat > version.txt <<EOF
HASH=%{package_git_long}
SHORTHASH=%{package_git_short}
DATE=$(date -u +'%Y-%m-%d %H:%M:%S %z')
EOF

export http_proxy=http://127.0.0.1

./configure \
    --arch=%{_target_cpu} \
    --build=build \
    --prefix=%{_prefix} \
    --enable-fdk-aac \
    --verbose

make -C build %{?_smp_mflags}

%install
%make_install -C build
desktop-file-validate %{buildroot}/%{_datadir}/applications/ghb.desktop
%find_lang ghb

%check
checksec --file %{buildroot}%{_bindir}/HandBrakeCLI
checksec --file %{buildroot}%{_bindir}/ghb

%files
%{_bindir}/HandBrakeCLI

%package gtk
Summary: HandBrake GUI
Conflicts: handbrake-legacy-gtk
Requires: handbrake
Requires: hicolor-icon-theme
Requires: desktop-file-utils
%description gtk
Things
%files -f ghb.lang gtk
%{_bindir}/ghb
%{_datadir}/applications/ghb.desktop
%{_datadir}/icons/hicolor/scalable/apps/hb-icon.svg
%post gtk
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
%postun gtk
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :
%posttrans gtk
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%changelog
* Sat Feb 13 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.0.0-2.b63b0bb
- Rebuild on new x265 library.

* Fri Feb 12 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.0.0-1.ba5eb77f
- Build HandBrake from master with external FFMPEG and everything. Up to date as of 2016-02-14 05:48:33 +0000. Cannot
  use the --enable-qsv flag because of our linking to a system FFMPEG: https://j.mp/1SphwL1
