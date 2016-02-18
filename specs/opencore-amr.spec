# FIXME I don't see the value in doing this right now, so postponing indefinitely.
#       AMR-NB comes from a few different places unfortunately, it's not nearly as clear as libvo-amrnbenc.
#       It is packaged in OpenCore-AMR like here, but also packaged separately in:
#       ftp://rpmfind.net/linux/rpmfusion/nonfree/fedora/development/rawhide/source/SRPMS/amrnb-11.0.0.0-2.fc22.src.rpm

%global _hardened_build 1

%define package_name libopencore-amr
%define package_version 0.1.3
%define package_release 1

Name:           %{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Summary:        VisualOn Adaptive Multi Rate Narrow Band audio codec.
License:        ASL 2.0
URL:            http://sourceforge.net/projects/opencore-amr/
Source0:        http://downloads.sourceforge.net/opencore-amr/opencore-amr/opencore-amr-%{package_version}.tar.gz

BuildRequires: checksec

%description
This library contains an encoder implementation of the Adaptive Multi Rate Narrowband (AMR-NB) audio codec. The library
is based on a codec implementation by VisualOn as part of the Stagefright framework from the Google Android project.

%prep

%setup -n opencore-amr-%{package_version}

%build
%configure \
    --with-pic \
    --enable-shared \
    --disable-static

make %{?_smp_mflags}

%install
%make_install

%check
checksec --file %{buildroot}%{_libdir}/libopencore-amrnb.so.0.0.3
checksec --file %{buildroot}%{_libdir}/libopencore-amrwb.so.0.0.3

%files
%{_libdir}/libopencore-amrnb.so.*
%{_libdir}/libopencore-amrwb.so.*
%exclude %{_libdir}/*.la

%package devel
Summary: Devel stuff for OpenCore AMR.
Requires: %{name} = %{version}
%description devel
Devel stuff for OpenCore AMR.
%files devel
%{_includedir}/opencore-amrnb/*.h
%{_includedir}/opencore-amrwb/*.h
%{_libdir}/libopencore-amrnb.so
%{_libdir}/libopencore-amrwb.so
%{_libdir}/pkgconfig/opencore-amrnb.pc
%{_libdir}/pkgconfig/opencore-amrwb.pc

%changelog
* Wed Feb 17 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 0.1.3-1
- Initial packaging.
