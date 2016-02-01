%global _hardened_build 1

%define package_name lame
%define package_version 3.99.5
%define package_release 1

Summary: LAME Ain't an MP3 Encoder.
Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
License: LGPL
Vendor: The LAME Project
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: http://www.mp3dev.org
Group: Applications/Multimedia
Source: lame-%{version}.tar.gz
Requires: ncurses >= 5.0

BuildRequires: ncurses-devel
BuildRequires: pkgconfig
BuildRequires: checksec
%ifarch %{ix86} x86_64
BuildRequires: nasm
%endif

%description
LAME Ain't an MP3 Encoder.

%prep
%setup

%build
sed -i -e 's/^\(\s*hardcode_libdir_flag_spec\s*=\).*/\1/' configure

%ifarch %{ix86}
export CFLAGS="$RPM_OPT_FLAGS -ffast-math"
sed -i -e '/xmmintrin\.h/d' configure
%endif

# configuration swiped from debian
%configure \
%ifarch %{ix86} x86_64
    --enable-nasm \
%endif
    --disable-rpath \
    --enable-expopt=full \
    --enable-dynamic-frontends \
    --with-fileio=lame
%{__make} %{?_smp_mflags} test CFLAGS="%{optflags}"

%install
%make_install
%{__ln_s} -f lame/lame.h %{buildroot}%{_includedir}/lame.h

%check
checksec --file frontend/.libs/lame
checksec --file libmp3lame/.libs/libmp3lame.so.0.0.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr (-,root,root)
%{_bindir}/lame
%{_prefix}/share/man/man1/lame.1.gz

%package -n libmp3lame
Summary: Shared libraries for LAME.
%description -n libmp3lame
Shared libraries for LAME.
%files -n libmp3lame
%{_libdir}/libmp3lame.so.*
%{_libdir}/libmp3lame.so
%exclude %{_libdir}/libmp3lame.a
%exclude %{_libdir}/libmp3lame.la

%package -n libmp3lame-devel
Summary: Shared libraries for LAME (development files).
Requires: libmp3lame = %{package_version}
%description -n libmp3lame-devel
Shared libraries for LAME (development files).
%files -n libmp3lame-devel
%defattr (-, root, root)
%doc API HACKING STYLEGUIDE
%{_includedir}/*
%{_prefix}/share/doc/lame/html/*.html

%changelog

* Mon Jan 11 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 3.99.5-1
- Repackaged for reasons.
