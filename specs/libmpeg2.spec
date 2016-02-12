%global _hardened_build 1

%define package_name libmpeg2
%define package_version 0.5.1
%define package_release 1

Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
Summary: MPEG-2 decoder libraries

Group: System Environment/Libraries
License: GPLv2+
URL: http://libmpeg2.sourceforge.net/
Source0: http://libmpeg2.sourceforge.net/files/libmpeg2-%{version}.tar.gz

BuildRequires: SDL-devel
BuildRequires: libXt-devel
BuildRequires: libXv-devel
BuildRequires: checksec
BuildRequires: chrpath

%description
libmpeg2 is a free library for decoding mpeg-2 and mpeg-1 video
streams. It is released under the terms of the GPL license.

%package -n mpeg2dec
Summary: MPEG-2 decoder program
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description -n mpeg2dec
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Provides: mpeg2dec-devel = %{version}-%{release}
Obsoletes: mpeg2dec-devel < %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure --disable-static \
%ifarch %{ix86} ppc
  --disable-accel-detect \
%endif

%install
%make_install
chrpath --delete %{buildroot}%{_bindir}/mpeg2dec

%check
checksec --file %{buildroot}%{_bindir}/corrupt_mpeg2
checksec --file %{buildroot}%{_bindir}/extract_mpeg2
checksec --file %{buildroot}%{_bindir}/mpeg2dec
checksec --file %{buildroot}%{_libdir}/libmpeg2.so.0.1.0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_libdir}/*.so.*

%files -n mpeg2dec
%defattr(-,root,root,-)
%{_bindir}/corrupt_mpeg2
%{_bindir}/extract_mpeg2
%{_bindir}/mpeg2dec
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root,-)
%doc CodingStyle doc/libmpeg2.txt doc/sample*.c
%{_includedir}/mpeg2dec/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmpeg2.pc
%{_libdir}/pkgconfig/libmpeg2convert.pc
%exclude %{_libdir}/libmpeg2.la
%exclude %{_libdir}/libmpeg2convert.la



%changelog
* Fri Feb 12 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 0.5.1-1
- Repackaged.
