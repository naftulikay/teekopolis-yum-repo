%global _hardened_build 1

%define package_name libxvidcore
%define package_version 1.3.4
%define package_release 1

Name: %{package_name}
Summary: A video decoder and encoder library aimed at providing the best compression efficiency and picture quality possible.
Version: %{package_version}
Release: %{package_release}%{?dist}
License: GPL
Source: http://downloads.xvid.org/downloads/xvidcore-%{package_version}.tar.bz2

%ifarch %{ix86} x86_64
BuildRequires: nasm
%endif

%description
A video decoder and encoder library aimed at providing the best compression efficiency and picture quality possible.

%prep

%setup -n xvidcore

%build
cd build/generic
%configure

make %{?_smp_mflags}

%install
%make_install -C build/generic
chmod +x %{buildroot}%{_libdir}/libxvidcore.so.*

%files
%{_libdir}/libxvidcore.so.*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary: libxvidcore-devel
Requires: libxvidcore = %{package_version}
%description devel
libxvidcore-devel
%files devel
%doc examples/
%{_includedir}/xvid.h
%{_libdir}/libxvidcore.so
%exclude %{_libdir}/libxvidcore.a
