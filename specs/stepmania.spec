%global _hardened_build 1

%define package_name stepmania
%define package_version 5.0.10
%define package_release 1

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
Summary: StepMania is a free dance and rhythm game for Windows, Mac, and Linux.
License: MIT
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: http://stepmania.com
Group: Applications/Multimedia
Source: https://github.com/stepmania/stepmania/archive/v%{package_version}.tar.gz#/stepmania-%{package_version}.tar.gz
Source1: https://github.com/ffmpeg/ffmpeg/archive/n2.1.3.tar.gz#/ffmpeg-linux-2.1.3.tar.gz
Patch0: stepmania-patch-0001-ffmpeg-pic.patch
Patch1: stepmania-patch-0002-cmake-i386.patch
Patch2: stepmania-patch-0003-static-libraries.patch

ExclusiveArch: %{ix86} x86_64

BuildRequires: alsa-lib-devel
BuildRequires: atk-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bash
BuildRequires: binutils
BuildRequires: bzip2-devel
BuildRequires: bzip2-libs
BuildRequires: cairo-devel
BuildRequires: cmake
BuildRequires: coreutils
BuildRequires: cpio
BuildRequires: diffutils
BuildRequires: dwz
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gdk-pixbuf2-devel
BuildRequires: glew-devel
BuildRequires: glib2-devel
BuildRequires: glibc
BuildRequires: glibc-common
BuildRequires: glibc-devel
BuildRequires: glibc-headers
BuildRequires: gtk2-devel
BuildRequires: json-c-devel
BuildRequires: jsoncpp-devel
BuildRequires: kernel-headers
BuildRequires: libX11-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libgcc
BuildRequires: libjpeg-turbo-devel
BuildRequires: libmad-devel
BuildRequires: libogg-devel
BuildRequires: libpng-devel
BuildRequires: libstdc++-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: libvorbis-devel
BuildRequires: m4
BuildRequires: make
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: pango-devel
BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: pulseaudio-libs-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: yasm
BuildRequires: git
BuildRequires: checksec
BuildRequires: libtomcrypt-devel
BuildRequires: libtommath-devel

Requires: gtk-update-icon-cache
Requires: hicolor-icon-theme
Requires: desktop-file-utils

Requires: atk
Requires: coreutils
Requires: dwz
Requires: elfutils
Requires: freetype
Requires: gdk-pixbuf2
Requires: glib2
Requires: glibc
Requires: glibc-common
Requires: gtk2
Requires: gzip
Requires: hostname
Requires: libGLEW
Requires: libX11
Requires: libXrandr
Requires: libgcc
Requires: libjpeg-turbo
Requires: libmad
Requires: libogg
Requires: libpng
Requires: libstdc++
Requires: libvorbis
Requires: mesa-libGL
Requires: mesa-libGLU
Requires: pango
Requires: pulseaudio-libs
Requires: pkgconfig

%description
StepMania is a free dance and rhythm game for Windows, Mac, and Linux. It features 3D graphics, keyboard and "dance pad"
support, and an editor for creating your own steps.

%prep

%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
sed -i 's:Exec=stepmania:Exec=/usr/share/stepmania-5.0/stepmania:g' stepmania.desktop

cp %{SOURCE1} extern/
( cd extern && tar xzf ffmpeg-linux-2.1.3.tar.gz && mv FFmpeg-n2.1.3 ffmpeg-linux-2.1.3 )

%build
export http_proxy=http://127.0.0.1

%cmake -G "Unix Makefiles" \
    -DCMAKE_INSTALL_PREFIX=/usr/share \
    -DCMAKE_SKIP_RPATH:BOOL=YES \
    -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=YES \
    -DENABLE_PIC:BOOL=ON \
    -DWITH_FULL_RELEASE:BOOL=ON \
    -DCMAKE_BUILD_TYPE=Release \
    .
make %{_smp_mflags}

%install
%make_install
test -d %{buildroot}%{_datadir} || mkdir %{buildroot}%{_datadir}
cp -r icons/ %{buildroot}%{_datadir}/icons
test -d %{buildroot}%{_datadir}/applications || mkdir %{buildroot}%{_datadir}/applications
install -m 0644 stepmania.desktop %{buildroot}%{_datadir}/applications/

%check
checksec --file %{buildroot}%{_datadir}/stepmania-5.0/stepmania
checksec --file %{buildroot}%{_datadir}/stepmania-5.0/GtkModule.so

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :
%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
# binary
%{_datadir}/stepmania-5.0/stepmania
%{_datadir}/stepmania-5.0/GtkModule.so
# assets
%{_datadir}/stepmania-5.0/Announcers
%{_datadir}/stepmania-5.0/BGAnimations
%{_datadir}/stepmania-5.0/BackgroundEffects
%{_datadir}/stepmania-5.0/BackgroundTransitions
%{_datadir}/stepmania-5.0/Characters
%{_datadir}/stepmania-5.0/Courses
%{_datadir}/stepmania-5.0/Data
%{_datadir}/stepmania-5.0/Docs
%{_datadir}/stepmania-5.0/NoteSkins
%{_datadir}/stepmania-5.0/Themes
%{_datadir}/stepmania-5.0/Scripts
%{_datadir}/stepmania-5.0/Songs
%{_datadir}/icons/hicolor/*/apps/stepmania-ssc.png
%{_datadir}/icons/hicolor/scalable/apps/stepmania-ssc.svg
%{_datadir}/applications/stepmania.desktop

%changelog
* Fri Feb 12 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 5.0.10-1
- Package StepMania. Everything looks great, but the GtkModule.so is missing a stack canary for some reason, and there's
  no binary in /usr/bin.
- Additionally, StepMania loathes using system libraries, so most things are statically compiled in now. It's better
  than segfaulting, but it's still bad.
- The build is kind of ugly due to it doing a Git checkout of a specific commit of FFMPEG and building it. It could be
  greatly improved by just using the tarball as a second RPM source and unpacking it in the right place.
