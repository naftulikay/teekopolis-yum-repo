# FIXME No PIE, no RELRO, no NX :(
# These files are binaries without symbols:
#
# makemkv-bin-%{version}/bin/amd64/makemkvcon
# makemkv-bin-%{version}/bin/i386/makemkvcon
# makemkv-bin-%{version}/bin/i386/mmdtsdec

# This is a binary image inserted in the compiled GUI binary:
# makemkv-oss-%{version}/makemkvgui/bin/image_data.bin

# mmdtsdec is a 32 bit only binary, so it is built only on i386 and required
# on x86_64.

%define package_name makemkv
%define package_version 1.9.9
%define package_release 3

Summary:        DVD and Blu-ray to MKV converter and network streamer.
Name:           %{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
License:        GuinpinSoft inc and Mozilla Public License Version 1.1 and LGPLv2.1+
URL:            http://www.makemkv.com/
ExclusiveArch:  %{ix86} x86_64

Source0:        http://www.makemkv.com/download/makemkv-oss-%{version}.tar.gz
Source1:        http://www.makemkv.com/download/makemkv-bin-%{version}.tar.gz

Patch0:         makemkv-patch-0001-oss-no-strip.patch

BuildRequires:  desktop-file-utils
BuildRequires:  expat-devel
BuildRequires:	openssl-devel
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:	qt4-devel

BuildRequires: checksec
BuildRequires: chrpath

Requires:       hicolor-icon-theme
%ifarch x86_64
Requires: mmdtsdec(%{__isa_name}-32)
%else
Requires: mmdtsdec%{_isa}
%endif

%description
MakeMKV is your one-click solution to convert video that you own into free and
patents-unencumbered format that can be played everywhere. MakeMKV is a format
converter, otherwise called "transcoder". It converts the video clips from
proprietary (and usually encrypted) disc into a set of MKV files, preserving
most information but not changing it in any way. The MKV format can store
multiple video/audio tracks with all meta-information and preserve chapters.

Additionally MakeMKV can instantly stream decrypted video without intermediate
conversion to wide range of players, so you may watch Blu-ray and DVD discs with
your favorite player on your favorite OS or on your favorite device.

%ifarch %{ix86}
%package -n mmdtsdec
Summary: MakeMKV DTS command line decoder.
%description -n mmdtsdec
MakeMKV is your one-click solution to convert video that you own into free and
patents-unencumbered format that can be played everywhere. MakeMKV is a format
converter, otherwise called "transcoder". It converts the video clips from
proprietary (and usually encrypted) disc into a set of MKV files, preserving
most information but not changing it in any way. The MKV format can store
multiple video/audio tracks with all meta-information and preserve chapters.

This package contains the DTS decoder command line tool.
%endif

%prep
%setup -q -T -c -n makemkv-%{version} -b 0 -b 1
pushd makemkv-oss-%{version}
%patch0 -p1
popd

%build
# accept eula
mkdir -p makemkv-bin-%{version}/tmp
echo "accepted" > makemkv-bin-%{version}/tmp/eula_accepted
cd makemkv-oss-%{version}
export CFLAGS="%{optflags} -D __STDC_FORMAT_MACROS"
%configure
make %{?_smp_mflags}

%install
make -C makemkv-oss-%{version} install DESTDIR=%{buildroot} LIBDIR=%{_libdir}
make -C makemkv-bin-%{version} install DESTDIR=%{buildroot} LIBDIR=%{_libdir}
chmod 755 %{buildroot}%{_libdir}/lib*.so*
desktop-file-validate %{buildroot}/%{_datadir}/applications/makemkv.desktop

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

cat > %{buildroot}%{_sysconfdir}/profile.d/makemkv.sh <<EOF
export LIBBDPLUS_PATH=%{_libdir}/libmmbd.so.0
export LIBAACS_PATH=%{_libdir}/libmmbd.so.0
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/makemkv.csh <<EOF
setenv LIBBDPLUS_PATH %{_libdir}/libmmbd.so.0
setenv LIBAACS_PATH %{_libdir}/libmmbd.so.0
EOF

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/mmdtsdec
chrpath --delete %{buildroot}%{_bindir}/makemkv
chrpath --delete %{buildroot}%{_bindir}/makemkvcon
chrpath --delete %{buildroot}%{_libdir}/libdriveio.so.0
chrpath --delete %{buildroot}%{_libdir}/libmakemkv.so.1
chrpath --delete %{buildroot}%{_libdir}/libmmbd.so.0

%ifarch x86_64
rm -f %{buildroot}/%{_bindir}/mmdtsdec
%endif

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/sbin/ldconfig

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%check
%ifarch %{ix86}
checksec --file %{buildroot}%{_bindir}/mmdtsdec
%endif
checksec --file %{buildroot}%{_bindir}/makemkv
checksec --file %{buildroot}%{_bindir}/makemkvcon
checksec --file %{buildroot}%{_libdir}/libdriveio.so.0
checksec --file %{buildroot}%{_libdir}/libmakemkv.so.1
checksec --file %{buildroot}%{_libdir}/libmmbd.so.0

%files
%doc makemkv-bin-%{version}/src/eula_en_linux.txt
%doc makemkv-oss-%{version}/License.txt
%config(noreplace) %{_sysconfdir}/profile.d/makemkv.*sh
%{_bindir}/makemkv
%{_bindir}/makemkvcon
%{_datadir}/MakeMKV
%{_datadir}/applications/makemkv.desktop
%{_datadir}/icons/hicolor/*/apps/makemkv.png
%{_libdir}/libdriveio.so.0
%{_libdir}/libmakemkv.so.1
%{_libdir}/libmmbd.so.0

%ifarch %{ix86}
%files -n mmdtsdec
%doc makemkv-bin-%{version}/src/eula_en_linux.txt
%{_bindir}/mmdtsdec
%endif

%changelog
* Thu Feb 18 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.9.9-3
- Strip rpath, add checksec to build.

* Wed Feb 03 2016 Naftuli Tzvi Kay <rfkrocktk@gmail.com> - 1.9.9-2
- Fix cross architecture dependencies.
