%global _hardened_build 1

%define package_name x264
%define package_version 148
%define package_release 20160201
%define package_buildtime 2245

Summary: The x264 H.264 video encoder.
Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
License: GPLv2
Vendor: VideoLAN
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: https://www.videolan.org/developers/x264.html
Group: Applications/Multimedia
Source: https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-%{package_release}-%{package_buildtime}-stable.tar.bz2
# FIXME x264 doesn't use libx264.so, it is still statically compiled
BuildRequires: yasm

%description
x264 H.264 Video Encoder

%prep

%setup -n x264-snapshot-%{package_release}-%{package_buildtime}-stable

%configure \
    --enable-pic \
    --disable-static \
    --enable-shared

%build
make %{?_smp_mflags}

%install

%make_install

%files
%{_bindir}/x264

%package -n libx264
Summary: x264 Shared Library
# description
%description -n libx264
x264 Shared Library
# files
%files -n libx264
%{_libdir}/libx264.so
%{_libdir}/libx264.so.*
# post
%post -n libx264 -p /sbin/ldconfig
%postun -n libx264 -p /sbin/ldconfig

%package -n libx264-devel
Summary: x264 Shared Library (Development Files)
Requires: libx264 = %{package_version}
# description
%description -n libx264-devel
x264 Shared Library (Development Files)
# files
%files -n libx264-devel
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/pkgconfig/x264.pc
