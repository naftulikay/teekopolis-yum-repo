%global _hardened_build 1

%define package_name libmfx
%define package_version
%define package_release 3
%define git_commit 9f4a84d73fb73d430f07a80cea3688c424439f6a
%define git_commit_short %(c=%{git_commit}; echo ${c:0:8})
%define realname mfx_dispatch

Name:           libmfx
Version:        1.16.0
Release:        %{package_release}.%{?git_commit_short}%{?dist}
Summary:        Intel Media SDK dispatcher library.
License:        Intel
URL:            https://github.com/lu-zero/mfx_dispatch
Source0:        https://github.com/lu-zero/mfx_dispatch/archive/%{git_commit}.tar.gz#/mfx_dispatch-%{git_commit_short}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libva-devel

Requires: libtool
Requires: libva

%description
Autotooled/Cmakified version of the open source Intel Media SDK dispatcher.

%prep
%setup -n mfx_dispatch-%{git_commit}
autoreconf -vif

%configure \
    --disable-static \
    --enable-shared \
    --with-libva_drm \
    --with-libva_x11

%build
make %{?_smp_mflags}


%install
%make_install

# create relative symlink to msdk for handbrake
( cd %{buildroot}%{_includedir} && ln -s mfx msdk)

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libmfx.so.*
%exclude %{_libdir}/libmfx.la

%package devel
Summary: Development files for libmfx.
Requires: libmfx = %{version}-%{release}
%description devel
The libmfx-devel package contains libraries and header files for
developing applications that use libmfx.
%files devel
%{_includedir}/*
%{_libdir}/libmfx.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Feb 03 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.16.0-3.9f4a84d7
- Moved the shared object symlink to the devel package as expected.

* Sun Dec 13 2015 Simone Caronni <negativo17@gmail.com> - 0.0.0-2.8220f46
- Fix build requirements.

* Fri Nov 27 2015 Simone Caronni <negativo17@gmail.com> 0.0.0-1.8220f46
- First build.
