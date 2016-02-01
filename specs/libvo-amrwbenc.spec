%global _hardened_build 1

%define package_name libvo-amrwbenc
%define package_version 0.1.3
%define package_release 1

Name:           %{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Summary:        VisualOn Adaptive Multi Rate Wideband audio codec.
License:        ASL 2.0
URL:            http://sourceforge.net/projects/opencore-amr/
Source0:        http://downloads.sourceforge.net/opencore-amr/vo-amrwbenc/vo-amrwbenc-%{package_version}.tar.gz

%description
This library contains an encoder implementation of the Adaptive Multi
Rate Wideband (AMR-WB) audio codec. The library is based on a codec
implementation by VisualOn as part of the Stagefright framework from
the Google Android project.

%prep
%setup -qn vo-amrwbenc-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING NOTICE
%doc ChangeLog
%{_libdir}/*.so
%{_libdir}/*.so.*
%exclude %{_libdir}/*.la

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%files devel
%{_includedir}/vo-amrwbenc/*.h
%{_libdir}/pkgconfig/vo-amrwbenc.pc

%changelog
* Tue Jan 19 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 0.1.3-1
- Repackaged.
