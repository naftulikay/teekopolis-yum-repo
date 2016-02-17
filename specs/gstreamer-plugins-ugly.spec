%global _hardened_build 1

%define package_name gstreamer-plugins-ugly
%define package_version 0.10.19
%define package_release 1

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
Summary: Ugly GStreamer plugins.
License: LGPL, but worse.
Source: https://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{package_version}.tar.xz
URL: https://gstreamer.freedesktop.org/modules/gst-plugins-ugly.html

BuildRequires: liba52-devel
BuildRequires: libdvdread-devel
BuildRequires: libmp3lame-devel
BuildRequires: libmad-devel
BuildRequires: libmpeg2-devel
BuildRequires: libvo-amrwbenc-devel
BuildRequires: libx264-devel

BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel

BuildRequires: checksec

%description
Ugly GStreamer plugins.

%prep

%setup -n gst-plugins-ugly-%{package_version}

%build
# TODO gstreamer-plugins-ugly needs heavy patching of its CDIO support to compile :-(
%configure \
    --enable-shared \
    --disable-rpath \
    --disable-cdio \
    --with-pic

make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/gstreamer-0.10/libgsta52dec.so
%{_libdir}/gstreamer-0.10/libgstasf.so
%{_libdir}/gstreamer-0.10/libgstdvdlpcmdec.so
%{_libdir}/gstreamer-0.10/libgstdvdread.so
%{_libdir}/gstreamer-0.10/libgstdvdsub.so
%{_libdir}/gstreamer-0.10/libgstiec958.so
%{_libdir}/gstreamer-0.10/libgstlame.so
%{_libdir}/gstreamer-0.10/libgstmad.so
%{_libdir}/gstreamer-0.10/libgstmpeg2dec.so
%{_libdir}/gstreamer-0.10/libgstmpegaudioparse.so
%{_libdir}/gstreamer-0.10/libgstmpegstream.so
%{_libdir}/gstreamer-0.10/libgstrmdemux.so
%{_libdir}/gstreamer-0.10/libgstx264.so
%{_datadir}/gstreamer-0.10/presets/*.prs
%{_datadir}/locale/*/LC_MESSAGES/gst-plugins-ugly-0.10.mo
%exclude %{_libdir}/gstreamer-0.10/*.la

%check
find %{buildroot} -iname '*.so' | sort | while read file ; do
    checksec --file $file
done

%changelog
* Tue Feb 16 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.7.1-1
- Packaged for the glorious City of Teekopolis.
- Why are we using such an old version? Because Fedora 23 packages GStreamer 0.10.36, a release from 2012.
