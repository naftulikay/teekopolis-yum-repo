%global _hardened_build 1

%define package_name libmad
%define package_version 0.15.1b
%define package_release 1

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
Summary: MAD: MPEG Audio Decoder
License: GPL
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: http://www.underbit.com/products/mad/
Source: http://downloads.sourceforge.net/mad/libmad/libmad-%{package_version}.tar.gz
Group: Applications/Multimedia

%description
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1 and the MPEG-2 extension to lower sampling
frequencies, as well as the de facto MPEG 2.5 format. All three audio layers — Layer I, Layer II, and Layer III (i.e.
MP3) — are fully implemented.

%prep

%setup

%build
%configure \
    --enable-debugging \
    --enable-accuracy \
    --with-pic

make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
%make_install

%files
%{_libdir}/libmad.so.*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%package devel
Summary: MAD: MPEG Audio Decoder
Requires: libmad = %{version}-%{release}
%description devel
Header files for libmad.
%files devel
%{_libdir}/libmad.so
%{_includedir}/mad.h
%exclude %{_libdir}/libmad.a
%exclude %{_libdir}/libmad.la

%changelog
* Sun Feb 07 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 0.15.1b-1
- Packaged for Teekopolis. Long live the glorious empire!
