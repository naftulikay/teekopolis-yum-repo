%global _hardened_build 1

%define package_name liba52
%define package_version 0.7.4
%define package_release 1

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
Summary: liba52 is a free library for decoding ATSC A/52 streams.
License: GPL
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: http://liba52.sourceforge.net/
Source: http://liba52.sourceforge.net/files/a52dec-%{package_version}.tar.gz
Group: Applications/Multimedia
BuildRequires: chrpath

%description
liba52 is a free library for decoding ATSC A/52 streams. It is released under the terms of the GPL license. The A/52
standard is used in a variety of applications, including digital television and DVD. It is also known as AC-3.

%prep

%setup -n a52dec-%{package_version}

%build
%configure \
    --enable-shared \
    --with-pic

make %{?_smp_mflags} CFLAGS="%{optflags}"
# die rpath die
chrpath --delete src/.libs/a52dec

%install
%make_install

%files
%{_libdir}/liba52.so.*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%package devel
Summary: liba52 is a free library for decoding ATSC A/52 streams (development files).
Requires: liba52 = %{version}-%{release}
%description devel
Header files for liba52.
%files devel
%{_libdir}/liba52.so
%{_includedir}/a52dec/*.h
%exclude %{_libdir}/liba52.a
%exclude %{_libdir}/liba52.la

%package -n a52dec
Summary: A/52 decoder binary.
%description -n a52dec
A/52 decoder binary.
%files -n a52dec
%{_bindir}/a52dec
%{_bindir}/extract_a52
%{_prefix}/share/man/man1/a52dec.1.gz
%{_prefix}/share/man/man1/extract_a52.1.gz

%changelog
* Sun Feb 07 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 0.7.4-1
- Packaged for Teekopolis. Long live the glorious empire!
