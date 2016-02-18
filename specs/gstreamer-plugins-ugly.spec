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

Patch0: gstreamer-plugins-ugly-patch-0001-fix-cdio.patch

BuildRequires: gettext-devel
BuildRequires: gtk-doc
BuildRequires: liba52-devel
BuildRequires: libcdio-devel
BuildRequires: libdvdnav-devel
BuildRequires: libdvdread-devel
BuildRequires: libid3tag-devel
BuildRequires: libmp3lame-devel
BuildRequires: libmad-devel
BuildRequires: libmpeg2-devel
BuildRequires: libsidplayfp-devel
BuildRequires: libvo-amrwbenc-devel
BuildRequires: libx264-devel
BuildRequires: orc-devel

BuildRequires: gstreamer-devel
BuildRequires: gstreamer-plugins-base-devel

Requires: gstreamer >= %{package_version}

BuildRequires: checksec

%description
Ugly GStreamer plugins.

%prep

%setup -n gst-plugins-ugly-%{package_version}
%patch0 -p1

%build
%configure \
    --enable-shared \
    --enable-debug \
    --enable-gtk-doc \
    --disable-static \
    --disable-rpath \
    --with-pic

make %{?_smp_mflags}

%install
%make_install
%find_lang gst-plugins-ugly-0.10

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f gst-plugins-ugly-0.10.lang
%doc AUTHORS COPYING README REQUIREMENTS
%{_libdir}/gstreamer-0.10/libgstcdio.so
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
%exclude %{_libdir}/gstreamer-0.10/*.la

%check
find %{buildroot} -iname '*.so' | sort | while read file ; do
    checksec --file $file
done

%package devel
Summary: Development stuff.
Requires: %{name} >= %{version}
%description devel
Development stuff.
%files devel
%{_datadir}/gtk-doc/html/gst-plugins-ugly-plugins-0.10/*

%changelog
* Tue Feb 16 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 0.10.19-1
- Packaged for the glorious City of Teekopolis.
