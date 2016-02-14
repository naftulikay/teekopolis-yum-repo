%global _hardened_build 1

%define package_name x265
%define package_version 1.9
%define package_release 1

Summary: x265 HEVC Video Encoder
Name: %{package_name}
Version: %{package_version}
Release: %{package_release}%{?dist}
License: GPLv2
Vendor: multicoreware
Packager: Naftuli Tzvi Kay <rfkrocktk@gmail.com>
URL: https://github.com/videolan/x265
Group: Applications/Multimedia
Source: https://download.videolan.org/pub/videolan/x265/x265_%{package_version}.tar.gz
Requires: libx265 = %{version}-%{release}
BuildRequires: yasm >= 1.3.0, cmake, ncurses-devel

Patch0: x265-patch-0001-pic.patch
Patch1: x265-patch-0002-test-shared.patch

%description
x265 HEVC Video Encoder

%prep

%setup -n x265_%{package_version}
%patch0 -p1
%patch1 -p1

%build
mkdir {8,10,12}bit

%ifarch x86_64
cd 12bit
%cmake -G "Unix Makefiles" \
    -DCMAKE_SKIP_RPATH:BOOL=YES \
    -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=YES \
    -DENABLE_PIC:BOOL=ON \
    -DENABLE_TESTS:BOOL=ON \
    -DHIGH_BIT_DEPTH:BOOL=ON \
    -DEXPORT_C_API:BOOL=OFF \
    -DENABLE_SHARED:BOOL=OFF \
    -DENABLE_CLI:BOOL=OFF \
    -DMAIN12:BOOL=ON \
    ../source
make %{?_smp_mflags} x265-static
cd ..

cd 10bit
%cmake -G "Unix Makefiles" \
    -DCMAKE_SKIP_RPATH:BOOL=YES \
    -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=YES \
    -DENABLE_PIC:BOOL=ON \
    -DENABLE_TESTS:BOOL=ON \
    -DHIGH_BIT_DEPTH:BOOL=ON \
    -DEXPORT_C_API:BOOL=OFF \
    -DENABLE_SHARED:BOOL=OFF \
    -DENABLE_CLI:BOOL=OFF \
    ../source
make %{?_smp_mflags} x265-static
cd ..
%endif

cd 8bit
%ifarch x86_64
ln -sf ../10bit/libx265.a libx265_main10.a
ln -sf ../12bit/libx265.a libx265_main12.a
%endif
%cmake -G "Unix Makefiles" \
    -DCMAKE_SKIP_RPATH:BOOL=YES \
    -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=YES \
    -DENABLE_PIC:BOOL=ON \
    -DENABLE_TESTS:BOOL=ON \
%ifarch x86_64
    -DEXTRA_LIB="x265_main10.a;x265_main12.a" \
    -DEXTRA_LINK_FLAGS=-L. \
    -DLINKED_10BIT:BOOL=ON \
    -DLINKED_12BIT:BOOL=ON \
%endif
    ../source

%ifarch x86_64
make %{?_smp_mflags} x265-static

mv libx265.a libx265_main.a

ar -M <<EOF
CREATE libx265.a
ADDLIB libx265_main.a
ADDLIB libx265_main10.a
ADDLIB libx265_main12.a
SAVE
END
EOF
%else
make %{?_smp_mflags} x265-shared
%endif

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} test/TestBench || :

%install
%make_install -C 8bit

%clean

# TODO x265 doesn't have man pages :(
%files
%{_bindir}/x265

# libx265 package
%package -n libx265
Summary: x265 Shared Library
# description
%description -n libx265
x265 Shared Library
# files
%files -n libx265
%{_libdir}/libx265.so.*
%exclude %{_libdir}/libx265.a
# post
%post -n libx265 -p /sbin/ldconfig
%postun -n libx265 -p /sbin/ldconfig

%package -n libx265-devel
Summary: x265 Shared Library (Development Files)
Requires: libx265 = %{package_version}
%description -n libx265-devel
x265 Shared Library (Development Files)
%files -n libx265-devel
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_libdir}/libx265.so
%{_libdir}/pkgconfig/x265.pc

%changelog
* Sat Feb 13 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.9-1
- Update to 1.9.

* Thu Feb 04 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.8-4
- Fix compilation for i386. x265 doesn't support high bit depth on 32-bit platforms, so compilation was failing.
  See: https://j.mp/1oaRTkx. Therefore, on i386, we compile in only 8-bit mode. If you're still on i386, buy a new
  computer. It's time.

* Wed Feb 03 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.8-3
- Moved the shared object symlink to the devel package as expected.

* Wed Feb 03 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.8-2
- Build shared library with all bit depths using some major crazy hacks. Default bit depth is 8, but bit depths are
  present for all depths (e.g. 10 and 12).
