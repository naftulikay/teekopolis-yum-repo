# UNSTABLE!
#
# FIXME many libraries are missing stack canary and only have partial relro :(
#       use overrides like `OPUS_CFLAGS="$CFLAGS"` and `OPUS_LIBS="$LDFLAGS"` to fix
# FIXME modplug and VP8 break compilation

%global _hardened_build 1

%define package_name gstreamer-plugins-bad
%define package_version 0.10.23
%define package_release 1

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
Summary: Bad GStreamer plugins.
License: LGPL, but worse.
Source: https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{package_version}.tar.xz
URL: https://gstreamer.freedesktop.org/modules/gst-plugins-bad.html

BuildRequires: schroedinger-devel
BuildRequires: libxvidcore-devel
BuildRequires: libvdpau-devel
BuildRequires: librsvg2-devel
BuildRequires: opus-devel
BuildRequires: opencv-devel
BuildRequires: openal-soft-devel
BuildRequires: bzip2-devel
BuildRequires: libvo-aacenc-devel
BuildRequires: libvo-amrwbenc-devel
BuildRequires: libass-devel
BuildRequires: libcurl-devel
BuildRequires: libdc1394-devel
BuildRequires: gsm-devel
BuildRequires: libfdk-aac-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libkate-devel
BuildRequires: libmpeg2-devel
BuildRequires: neon-devel
BuildRequires: SDL-devel
BuildRequires: libsndfile-devel
BuildRequires: libtimidity-devel
BuildRequires: libcdaudio-devel
BuildRequires: libmpcdec-devel

BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel

BuildRequires: checksec
BuildRequires: chrpath

%description
Bad GStreamer plugins.

%prep

%setup -n gst-plugins-bad-%{package_version}

%build
%configure \
    --enable-shared \
    --disable-rpath \
    --disable-modplug \
    --disable-vp8 \
    --with-pic

make %{?_smp_mflags}

%install
%make_install

chrpath --delete %{buildroot}%{_libdir}/gstreamer-0.10/*.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
# libraries
%{_libdir}/*.so.*
%{_libdir}/gstreamer-0.10/libgst*.so
# headers
%{_includedir}/gstreamer-0.10/gst/*
# presets
%{_datadir}/gstreamer-0.10/presets/*.prs
# l10n
%{_datadir}/locale/*/LC_MESSAGES/gst-plugins-bad-0.10.mo
# excludes
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%exclude %{_libdir}/gstreamer-0.10/*.a
%exclude %{_libdir}/gstreamer-0.10/*.la
%exclude %{_datadir}/glib-2.0/schemas/org.freedesktop.gstreamer-0.10.default-elements.gschema.xml

%package devel
Summary: Devel stuff.
%description devel
Devel stuff
%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/gst-plugins-bad-libs-0.10

%check
find %{buildroot} -type f -iname '*.so*' | sort | while read file ; do
    checksec --file $file
done

%changelog
* Tue Feb 16 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.7.1-1
- Packaged for the glorious City of Teekopolis.
- Why are we using such an old version? Because Fedora 23 packages GStreamer 0.10.36, a release from 2012.
