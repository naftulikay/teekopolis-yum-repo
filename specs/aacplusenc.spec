%global _hardened_build 1

%define package_name aacplusenc
%define package_version 2.0.2
%define package_release 1

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
Summary: AAC+ encoder.
License: LGPL, but worse.
Source0: http://ffmpeg.gusari.org/uploads/libaacplus-2.0.2.tar.gz
Source1: http://www.3gpp.org/ftp/Specs/archive/26_series/26.410/26410-800.zip
URL: http://tipok.org.ua/node/17

Requires: libaacplus

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: fftw
BuildRequires: libtool

%description
AAC+ encoder.

%prep
%setup -n libaacplus-%{package_version}
cp %{SOURCE1} src/26410-800.zip

%build
export http_proxy=http://127.0.0.1
autoreconf -vif
%configure --disable-static
make

%install
%make_install

%files
%{_bindir}/aacplusenc
%{_prefix}/share/man/man1/aacplusenc.1.gz

%package -n libaacplus
Summary: libaacplus
%description -n libaacplus
libaacplus
%files -n libaacplus
%{_libdir}/libaacplus.so
%{_libdir}/libaacplus.so.*
%exclude %{_libdir}/libaacplus.la
%post -n libaacplus -p /sbin/ldconfig
%postun -n libaacplus -p /sbin/ldconfig

%package -n libaacplus-devel
Summary: libaacplus-devel
%description -n libaacplus-devel
libaacplus-devel
%files -n libaacplus-devel
%{_includedir}/aacplus.h
%{_libdir}/pkgconfig/aacplus.pc
