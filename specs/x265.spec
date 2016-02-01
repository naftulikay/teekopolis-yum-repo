%global _hardened_build 1

%define package_name x265
%define package_version 1.8
%define package_release 1

Summary: x265 HEVC Video Encoder
Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
License: GPLv2
Vendor: multicoreware
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: https://github.com/videolan/x265
Group: Applications/Multimedia
Source: https://download.videolan.org/pub/videolan/x265/x265_1.8.tar.gz
Requires: libx265 = %{package_version}
BuildRequires: yasm >= 1.3.0, cmake, ncurses-devel

Patch0: x265-patch-0001-pic.patch
Patch1: x265-patch-0002-test-shared.patch

%description
x265 HEVC Video Encoder

%prep

%setup -n x265_%{package_version}
%patch0 -p1
%patch1 -p1

%build
%cmake -G "Unix Makefiles" \
    -DCMAKE_SKIP_RPATH:BOOL=YES \
    -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=YES \
    -DENABLE_PIC:BOOL=ON \
    -DENABLE_TESTS:BOOL=ON \
    source
make %{?_smp_mflags} x265-shared

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} test/TestBench || :

%install
%make_install

%clean

# TODO x265 doesn't have man pages :(
%files
%{_bindir}/x265

# libx265 package
%package -n libx265
Summary: x265 Shared Library
# description
%description -n libx265
x265 Shared Library
# files
%files -n libx265
%{_libdir}/libx265.so
%{_libdir}/libx265.so.*
%exclude %{_libdir}/libx265.a
# post
%post -n libx265 -p /sbin/ldconfig
%postun -n libx265 -p /sbin/ldconfig

%package -n libx265-devel
Summary: x265 Shared Library (Development Files)
Requires: libx265 = %{package_version}
%description -n libx265-devel
x265 Shared Library (Development Files)
%files -n libx265-devel
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_libdir}/pkgconfig/x265.pc
