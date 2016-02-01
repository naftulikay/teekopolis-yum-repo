%global _hardened_build 1

%define package_name ffmpeg
%define package_version 2.8.5
%define package_release 1
%define package_epoch 1

Summary: A complete, cross-platform solution to record, convert, and stream audio and video.
Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
License: LGPL
Vendor: The FFPMEG Project
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: https://ffmpeg.org
Group: Applications/Multimedia
Source: https://ffmpeg.org/releases/ffmpeg-%{package_version}.tar.xz

# build-time requirements
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: doxygen
BuildRequires: texinfo
# text/subtitle libraries
BuildRequires: freetype-devel
BuildRequires: fribidi-devel
BuildRequires: libass-devel
# portable media i/o libraries
BuildRequires: libcdio-paranoia-devel
BuildRequires: libbluray-devel
BuildRequires: libdc1394-devel
# compression libraries
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
# transport libraries
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
BuildRequires: libssh-devel
# audio libraries
BuildRequires: gsm-devel
BuildRequires: libmp3lame-devel
BuildRequires: opus-devel
BuildRequires: libogg-devel
BuildRequires: libvorbis-devel
BuildRequires: libtheora-devel
BuildRequires: speex-devel
BuildRequires: soxr-devel
BuildRequires: libmodplug-devel
BuildRequires: openal-soft-devel
BuildRequires: libfdk-aac-devel
BuildRequires: libaacplus
BuildRequires: libaacplus-devel
BuildRequires: libvo-aacenc-devel
BuildRequires: libvo-amrwbenc-devel
# video libraries
BuildRequires: libvpx-devel
BuildRequires: libx264-devel
BuildRequires: libx265-devel
BuildRequires: schroedinger-devel
BuildRequires: libxvidcore-devel
# video effect libraries
BuildRequires: frei0r-devel
# graphics libraries
BuildRequires: libwebp-devel
# acceleration libraries
BuildRequires: opencl-headers
BuildRequires: ocl-icd-devel
BuildRequires: libmfx-devel
# linux plugins
BuildRequires: SDL-devel
BuildRequires: libv4l-devel
BuildRequires: libvdpau-devel
BuildRequires: pulseaudio-libs-devel

%ifarch %{ix86} x86_64
BuildRequires:  libXvMC-devel
BuildRequires:  libva-devel
BuildRequires:  yasm
%endif

%description
A complete, cross-platform solution to record, convert, and stream audio and video.

%prep -q

%setup -q

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

./configure \
    --arch=%{_target_cpu} \
    --disable-debug \
    --disable-static \
    --disable-stripping \
    --enable-libaacplus \
    --enable-avfilter \
    --enable-avresample \
    --enable-bzlib \
    --enable-doc \
    --enable-fontconfig \
    --enable-frei0r \
    --enable-gnutls \
    --enable-gpl \
    --enable-iconv \
    --enable-libass \
    --enable-libbluray \
    --enable-libcdio \
    --enable-libdc1394 \
    --enable-libfdk-aac \
    --enable-libfreetype \
    --enable-libfribidi \
    --enable-libgsm \
    --disable-libkvazaar \
    --enable-libmfx \
    --enable-libmp3lame \
    --enable-libopus \
    --enable-libpulse \
    --enable-libschroedinger \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libssh \
    --enable-libtheora \
    --enable-libv4l2 \
    --enable-libvorbis \
    --enable-libvo-aacenc \
    --enable-libvo-amrwbenc \
    --enable-libvpx \
    --enable-libwebp \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libxvid \
    --enable-lzma \
    --enable-nonfree \
    --enable-openal \
    --enable-opencl \
    --enable-opengl \
    --enable-postproc \
    --enable-pthreads \
    --enable-sdl \
    --enable-shared \
    --enable-version3 \
    --enable-x11grab \
    --enable-xlib \
    --enable-zlib \
    --enable-pic \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --datadir=%{_datadir}/%{name} \
    --incdir=%{_prefix}/include \
    --libdir=%{_libdir} \
    --shlibdir=%{_libdir} \
    --docdir=%{_prefix}/share/doc/ffmpeg \
    --mandir=%{_prefix}/share/man \
    --optflags="%{optflags}" \
%ifarch %{ix86}
    --cpu=%{_target_cpu} \
%endif
%ifarch %{ix86} x86_64 ppc ppc64
    --enable-runtime-cpudetect \
%endif
%ifarch ppc
    --cpu=g3 \
%endif
%ifarch ppc64
    --cpu=g5 \
%endif
%ifarch %{arm}
    --disable-runtime-cpudetect --arch=arm \
%ifarch armv6hl
    --cpu=armv6 \
%else
    --enable-thumb \
%endif
%ifarch armv7hnl
    --enable-neon \
%endif
%endif

make %{?_smp_mflags}

%install
%make_install

%files
%{_bindir}/ffmpeg
%{_bindir}/ffplay
%{_bindir}/ffprobe
%{_bindir}/ffserver
%{_prefix}/share/man/man1/ffmpeg.1.gz
%{_prefix}/share/man/man1/ffmpeg-all.1.gz
%{_prefix}/share/man/man1/ffmpeg-bitstream-filters.1.gz
%{_prefix}/share/man/man1/ffmpeg-codecs.1.gz
%{_prefix}/share/man/man1/ffmpeg-devices.1.gz
%{_prefix}/share/man/man1/ffmpeg-filters.1.gz
%{_prefix}/share/man/man1/ffmpeg-formats.1.gz
%{_prefix}/share/man/man1/ffmpeg-protocols.1.gz
%{_prefix}/share/man/man1/ffmpeg-resampler.1.gz
%{_prefix}/share/man/man1/ffmpeg-scaler.1.gz
%{_prefix}/share/man/man1/ffmpeg-utils.1.gz
%{_prefix}/share/man/man1/ffplay.1.gz
%{_prefix}/share/man/man1/ffplay-all.1.gz
%{_prefix}/share/man/man1/ffprobe.1.gz
%{_prefix}/share/man/man1/ffprobe-all.1.gz
%{_prefix}/share/man/man1/ffserver.1.gz
%{_prefix}/share/man/man1/ffserver-all.1.gz
%{_prefix}/share/ffmpeg/*.ffpreset

%package -n ffmpeg-docs
Summary: HTML documentation for FFMPEG and its libraries
%description -n ffmpeg-docs
ffmpeg-docs
%files -n ffmpeg-docs
%exclude %{_prefix}/share/ffmpeg/ffprobe.xsd
%{_prefix}/share/doc/ffmpeg/*.html

%package -n ffmpeg-examples
Summary: ffmpeg-examples
%description -n ffmpeg-examples
ffmpeg-examples
%files -n ffmpeg-examples
%{_prefix}/share/ffmpeg/examples/*

%package -n ffmpeg-devel
Summary: ffmpeg-devel
Requires: ffmpeg-docs
Requires: ffmpeg-examples
Requires: libavcodec-devel
Requires: libavdevice-devel
Requires: libavfilter-devel
Requires: libavformat-devel
Requires: libavresample-devel
Requires: libavutil-devel
Requires: libpostproc-devel
Requires: libswresample-devel
Requires: libswscale-devel
%description -n ffmpeg-devel
ffmpeg-devel
%files -n ffmpeg-devel
%exclude /*

%package -n libavcodec
Summary: libavcodec
%description -n libavcodec
libavcodec
%files -n libavcodec
%{_libdir}/libavcodec.so.*

%package -n libavcodec-devel
Summary: libavcodec
Requires: libavcodec
%description -n libavcodec-devel
libavcodec
%files -n libavcodec-devel
%{_includedir}/libavcodec/*.h
%{_libdir}/libavcodec.so
%{_libdir}/pkgconfig/libavcodec.pc
%{_prefix}/share/man/man3/libavcodec.3.gz

%package -n libavdevice
Summary: libavdevice
%description -n libavdevice
libavdevice
%files -n libavdevice
%{_libdir}/libavdevice.so.*

%package -n libavdevice-devel
Summary: libavdevice-devel
Requires: libavdevice
%description -n libavdevice-devel
libavdevice
%files -n libavdevice-devel
%{_includedir}/libavdevice/*.h
%{_libdir}/libavdevice.so
%{_libdir}/pkgconfig/libavdevice.pc
%{_prefix}/share/man/man3/libavdevice.3.gz

%package -n libavfilter
Summary: libavfilter
%description -n libavfilter
libavfilter
%files -n libavfilter
%{_libdir}/libavfilter.so.*

%package -n libavfilter-devel
Summary: libavfilter-devel
Requires: libavfilter
%description -n libavfilter-devel
libavfilter-devel
%files -n libavfilter-devel
%{_includedir}/libavfilter/*.h
%{_libdir}/libavfilter.so
%{_libdir}/pkgconfig/libavfilter.pc
%{_prefix}/share/man/man3/libavfilter.3.gz

%package -n libavformat
Summary: libavformat
%description -n libavformat
libavformat
%files -n libavformat
%{_libdir}/libavformat.so.*

%package -n libavformat-devel
Summary: libavformat-devel
Requires: libavformat
%description -n libavformat-devel
libavformat-devel
%files -n libavformat-devel
%{_includedir}/libavformat/*.h
%{_libdir}/libavformat.so
%{_libdir}/pkgconfig/libavformat.pc
%{_prefix}/share/man/man3/libavformat.3.gz

%package -n libavresample
Summary: libavresample
%description -n libavresample
libavresample
%files -n libavresample
%{_libdir}/libavresample.so.*

%package -n libavresample-devel
Summary: libavresample-devel
Requires: libavresample
%description -n libavresample-devel
libavresample
%files -n libavresample-devel
%{_includedir}/libavresample/*.h
%{_libdir}/libavresample.so
%{_libdir}/pkgconfig/libavresample.pc

%package -n libavutil
Summary: libavutil
%description -n libavutil
libavutil
%files -n libavutil
%{_libdir}/libavutil.so.*

%package -n libavutil-devel
Summary: libavutil-devel
Requires: libavutil
%description -n libavutil-devel
libavutil-devel
%files -n libavutil-devel
%{_includedir}/libavutil/*.h
%{_libdir}/libavutil.so
%{_libdir}/pkgconfig/libavutil.pc
%{_prefix}/share/man/man3/libavutil.3.gz

%package -n libpostproc
Summary: libpostproc
%description -n libpostproc
libpostproc
%files -n libpostproc
%{_libdir}/libpostproc.so.*

%package -n libpostproc-devel
Summary: libpostproc-devel
Requires: libpostproc
%description -n libpostproc-devel
libpostproc-devel
%files -n libpostproc-devel
%{_includedir}/libpostproc/*.h
%{_libdir}/libpostproc.so
%{_libdir}/pkgconfig/libpostproc.pc

%package -n libswresample
Summary: libswresample
%description -n libswresample
libswresample
%files -n libswresample
%{_libdir}/libswresample.so.*

%package -n libswresample-devel
Summary: libswresample-devel
Requires: libswresample
%description -n libswresample-devel
libswresample-devel
%files -n libswresample-devel
%{_includedir}/libswresample/*.h
%{_libdir}/libswresample.so
%{_libdir}/pkgconfig/libswresample.pc
%{_prefix}/share/man/man3/libswresample.3.gz

%package -n libswscale
Summary: libswscale
%description -n libswscale
libswscale
%files -n libswscale
%{_libdir}/libswscale.so.*

%package -n libswscale-devel
Summary: libswscale-devel
Requires: libswscale
%description -n libswscale-devel
libswscale-devel
%files -n libswscale-devel
%{_includedir}/libswscale/*.h
%{_libdir}/libswscale.so
%{_libdir}/pkgconfig/libswscale.pc
%{_prefix}/share/man/man3/libswscale.3.gz
