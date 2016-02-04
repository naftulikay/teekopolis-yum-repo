%global _hardened_build 1

%define package_name libfdk-aac
%define package_version 0.1.4
%define package_release 2

Name:           %{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Summary:        asdasd

License:        ASL 2.0
URL:            http://sourceforge.net/projects/opencore-amr/
Source0:        http://downloads.sourceforge.net/opencore-amr/fdk-aac/fdk-aac-%{package_version}.tar.gz

%description
Advanced Audio Coding Decoder/Encoder Library.

%prep
%setup -n fdk-aac-%{package_version}

%build

%configure --disable-static

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license NOTICE
%doc ChangeLog
%{_libdir}/libfdk-aac.so.*
%exclude %{_libdir}/libfdk-aac.la

%package        devel
Summary:        Development files for libfdk-aac.
Requires:       %{package_name}
%description    devel
The libfdk-devel package contains libraries and header files for
developing applications that use libfdk-aac.
%files devel
%doc documentation/*
%{_includedir}/*
%{_libdir}/libfdk-aac.so
%{_libdir}/pkgconfig/fdk-aac.pc

%changelog
* Wed Feb 03 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 0.1.4-2
- Moved the shared object symlink to the devel package as expected.

* Fri Nov 13 2015 Simone Caronni <negativo17@gmail.com> - 0.1.4-1
- First build.
