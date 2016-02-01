%global _hardened_build 1

%define package_name libvo-aacenc
%define package_version 0.1.3
%define package_release 2

Name:           %{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Summary:        VisualOn AAC encoder library
License:        ASL 2.0
URL:            http://sourceforge.net/projects/opencore-amr/
Source0:        http://downloads.sourceforge.net/opencore-amr/vo-aacenc/vo-aacenc-%{package_version}.tar.gz

%description
This library contains an encoder implementation of the Advanced Audio
Coding (AAC) audio codec. The library is based on a codec implementation
by VisualOn as part of the Stagefright framework from the Google
Android project.

%prep
%setup -qn vo-aacenc-%{version}

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
%{_includedir}/vo-aacenc/*.h
%{_libdir}/pkgconfig/vo-aacenc.pc

%changelog
* Tue Jan 19 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 0.1.3-2
- Repackaged.
* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 0.1.3-1
- First build.
