%global _hardened_build 1

%define package_name libdvdcss
%define package_version 1.2.13
%define package_release 1

Summary:        A portable abstraction library for DVD decryption
Name:           %{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
License:        GPLv2+
URL:            https://www.videolan.org/%{name}/
Source:         https://download.videolan.org/pub/%{name}/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  doxygen

BuildRequires: checksec

Requires(post): ldconfig

%description
This is a portable abstraction library for DVD decryption which is used by
the VideoLAN project, a full MPEG2 client/server solution.  You will need
to install this package in order to have encrypted DVD playback with the
VideoLAN client and the Xine navigation plugin.

%package devel
Summary:     Header files and development libraries for %{name}
Requires:    %{name} = %{version}-%{release}
Requires:    pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q

%build
%configure
make %{_smp_mflags}

%install
%make_install
rm -fr %{buildroot}%{_docdir}/%{name}

%check
checksec --file %{buildroot}%{_libdir}/libdvdcss.so.2.1.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING ChangeLog README NEWS
%exclude %{_libdir}/%{name}.a
%exclude %{_libdir}/%{name}.la
%{_libdir}/libdvdcss.so.*

%files devel
%doc doc/html
%{_includedir}/dvdcss
%{_libdir}/libdvdcss.so
%{_libdir}/pkgconfig/libdvdcss.pc

%changelog
* Thu Mar 10 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.2.13-1
- Revert to an earlier version which works for me on Ubuntu.

* Wed Feb 03 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.4.0-2
- Moved the shared object symlink to the devel package as expected.

* Mon Jan 11 2016 Naftuli Kay <rfkrocktk@gmail.com> - 1.4.0-1
- Update to 1.4.0.
- Forked the upstream repository, building it for myself now.

* Sat Oct 31 2015 Simone Caronni <negativo17@gmail.com> - 1.3.99-1
- Update to 1.3.99.

* Fri Oct 24 2014 Simone Caronni <negativo17@gmail.com> - 1.3.0-1
- Update to 1.3.0.
- Remove RHEL 5 obsolete tags from SPEC file.

* Fri Nov 15 2013 Simone Caronni <negativo17@gmail.com> - 1.2.13-2
- Run ldconfig in scriptlets.

* Tue May 07 2013 Simone Caronni <negativo17@gmail.com> - 1.2.13-1
- Update to 1.2.13.
- Add doxygen docs in devel subpackage.

* Mon Mar 12 2012 Remi Collet <RPMS@famillecollet.com> - 1.2.12-1
- Update to 1.2.12

* Sat Feb 18 2012 Remi Collet <RPMS@famillecollet.com> - 1.2.11-2
- If unsure, assume the drive is of RPC-I type

* Tue Nov 22 2011 Remi Collet <RPMS@famillecollet.com> - 1.2.11-1
- Update to 1.2.11
