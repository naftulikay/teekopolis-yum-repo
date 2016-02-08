%global _hardened_build 1

%define package_name x264
%define package_version 148
%define package_release 4
%define package_builddate 20160203
%define package_buildtime 2245

Summary: The x264 H.264 video encoder.
Name: %{package_name}
Version: %{package_version}
Release: %{package_release}.%{package_builddate}%{?dist}
License: GPLv2
Vendor: VideoLAN
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: https://www.videolan.org/developers/x264.html
Group: Applications/Multimedia
Source: https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-%{package_builddate}-%{package_buildtime}-stable.tar.bz2
Requires: libx264 = %{version}-%{release}
BuildRequires: yasm

%description
x264 H.264 Video Encoder

%prep

%setup -n x264-snapshot-%{package_builddate}-%{package_buildtime}-stable

%build
%configure \
    --enable-debug \
    --enable-pic \
    --enable-shared \
    --system-libx264 \
    --bit-depth=10

# compile shared library to libx264_main10.so.$version
sed -i -e 's:SONAME=libx264\.so\.\([0-9]\{1,\}\):SONAME=libx264_main10.so.\1:g' config.mak

make %{?_smp_mflags}

%configure \
    --enable-debug \
    --enable-pic \
    --enable-shared \
    --system-libx264 \
    --bit-depth=8

make %{?_smp_mflags}

%install
%make_install
install -m 0755 libx264_main10.so.* %{buildroot}%{_libdir}/
( cd %{buildroot}%{_libdir} && ln -sf libx264_main10.so.* libx264_main10.so )

%files
%{_bindir}/x264

%package -n libx264
Summary: x264 Shared Library
# description
%description -n libx264
x264 Shared Library
# files
%files -n libx264
%{_libdir}/libx264.so.*
%{_libdir}/libx264_main10.so.*
# post
%post -n libx264 -p /sbin/ldconfig
%postun -n libx264 -p /sbin/ldconfig

%package -n libx264-devel
Summary: x264 Shared Library (Development Files)
Requires: libx264 = %{version}-%{release}
# description
%description -n libx264-devel
x264 Shared Library (Development Files)
# files
%files -n libx264-devel
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/libx264.so
%{_libdir}/libx264_main10.so
%{_libdir}/pkgconfig/x264.pc

%changelog
* Thu Feb 04 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 148-3.20160203
- Have the binary link to libx264.so instead of statically being compiled.

* Wed Feb 03 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 148-20160203
- Moved the shared object symlink to the devel package as expected.
