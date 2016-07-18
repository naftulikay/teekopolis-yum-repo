%global _hardened_build 1

%define package_name gstreamer1-plugins-libav
%define package_version 1.8.2
%define package_release 1

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
Summary: Ugly GStreamer plugins.
License: LGPL, but worse.
Source: https://gstreamer.freedesktop.org/src/gst-libav/gst-libav-%{package_version}.tar.xz
URL: https://gstreamer.freedesktop.org/modules/gst-plugins-ugly.html

BuildRequires: gettext-devel
BuildRequires: gtk-doc

BuildRequires: ffmpeg-devel

BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel

BuildRequires: checksec

Requires: gstreamer1 >= %{package_version}

%description
libav plugin for GStreamer.

%prep

%setup -n gst-libav-%{package_version}

%build
%configure \
    --enable-shared \
    --enable-debug \
    --enable-gtk-doc \
    --disable-static \
    --disable-rpath \
    --with-pic \
    --with-system-libav

make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/gstreamer-1.0/libgstlibav.so
%exclude %{_libdir}/gstreamer-1.0/*.la

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
%{_datadir}/gtk-doc/html/gst-libav-plugins-1.0/*

%changelog
* Sun Jul 17 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.8.2-1
  Repackage for Fedora 24.

* Wed Feb 17 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.6.3-1
- Initial packaging.
