%define revision 106587
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define basever 15.0.865.0
%define patchver() ([ -f %{_sourcedir}/patch-%1-%2.diff.xz ] || exit 1; xz -dc %{_sourcedir}/patch-%1-%2.diff.xz|patch -p1);

Name: chromium-browser-stable
Version: 15.0.874.102
Release: %mkrel 1
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL
Source0: chromium-%{basever}.tar.xz
Source1: chromium-wrapper
Source2: chromium-browser.desktop
Source3: attributed_string_coder.h
Source1000: patch-15.0.865.0-15.0.874.1.diff.xz
Source1001: binary-15.0.865.0-15.0.874.1.tar.xz
Source1002: script-15.0.865.0-15.0.874.1.sh
Source1003: patch-15.0.874.1-15.0.874.12.diff.xz
Source1004: patch-15.0.874.12-15.0.874.15.diff.xz
Source1005: patch-15.0.874.15-15.0.874.21.diff.xz
Source1006: patch-15.0.874.21-15.0.874.51.diff.xz
Source1007: binary-15.0.874.21-15.0.874.51.tar.xz
Source1008: patch-15.0.874.51-15.0.874.54.diff.xz
Source1009: patch-15.0.874.54-15.0.874.81.diff.xz
Source1010: binary-15.0.874.54-15.0.874.81.tar.xz
Source1011: patch-15.0.874.81-15.0.874.92.diff.xz
Source1012: patch-15.0.874.92-15.0.874.100.diff.xz
Source1013: patch-15.0.874.100-15.0.874.102.diff.xz
Patch0: chromium-15.0.874.1-skip-builder-tests.patch
Patch1: chromium-14.0.835.0-gcc46.patch
Provides: %{crname}
Conflicts: chromium-browser-unstable
Conflicts: chromium-browser-beta
Obsoletes: chromium-browser < 1:9.0.597.94
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bison, flex, gtk2-devel, atk-devel, libexpat-devel, gperf
BuildRequires: libnspr-devel, libnss-devel, libalsa-devel
BuildRequires: libglib2-devel, libbzip2-devel, libz-devel, libpng-devel
BuildRequires: libjpeg-devel, libmesagl-devel, libmesaglu-devel
BuildRequires: libxscrnsaver-devel, libdbus-glib-devel, libcups-devel
BuildRequires: libgnome-keyring-devel libvpx-devel libxtst-devel
BuildRequires: libxslt-devel libxml2-devel libxt-devel libpam-devel
BuildRequires: libevent-devel libflac-devel libpulseaudio-devel
BuildRequires: libelfutils-devel
ExclusiveArch: i586 x86_64 armv7l

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-browser-unstable package instead.

Note: If you are reverting from unstable to stable or beta channel, you may
experience tab crashes on startup. This crash only affects tabs restored
during the first launch due to a change in how tab state is stored.
See http://bugs.chromium.org/34688. It's always a good idea to back up
your profile before changing channels.

%package -n chromium-browser
Summary: A fast webkit-based web browser (transition package)
Epoch: 1
Group: Networking/WWW
Requires: %{name} = %{version}-%{release}

%description -n chromium-browser
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is a transition package that installs the stable channel Chromium
browser. If you prefer the dev channel browser, install the
chromium-browser-unstable package instead.


%prep
%setup -q -n chromium-%{basever}
install -D %{_sourcedir}/attributed_string_coder.h \
	chrome/common/mac/attributed_string_coder.h
%patchver 15.0.865.0 15.0.874.1
tar xvf %{_sourcedir}/binary-15.0.865.0-15.0.874.1.tar.xz
sh -x %{_sourcedir}/script-15.0.865.0-15.0.874.1.sh
%patchver 15.0.874.1 15.0.874.12
rm net/data/ssl/certificates/unosoft_hu_cert.der
%patchver 15.0.874.12 15.0.874.15
%patchver 15.0.874.15 15.0.874.21
%patchver 15.0.874.21 15.0.874.51
tar xvf %{_sourcedir}/binary-15.0.874.21-15.0.874.51.tar.xz
%patchver 15.0.874.51 15.0.874.54
%patchver 15.0.874.54 15.0.874.81
tar xvf %{_sourcedir}/binary-15.0.874.54-15.0.874.81.tar.xz
%patchver 15.0.874.81 15.0.874.92
%patchver 15.0.874.92 15.0.874.100
%patchver 15.0.874.100 15.0.874.102

%patch0 -p1 -b .skip-builder-tests
%patch1 -p1 -b .gcc46
echo "%{revision}" > build/LASTCHANGE.in

sed -i -e '/test_support_common/s/^/#/' \
	chrome/browser/sync/tools/sync_tools.gyp

# Hard code extra version
FILE=chrome/common/chrome_version_info_linux.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

%build
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
	-D linux_sandbox_path=%{_crdir}/chrome-sandbox \
	-D linux_sandbox_chrome_path=%{_crdir}/chrome \
	-D linux_link_gnome_keyring=0 \
	-D use_gconf=0 \
	-D werror='' \
	-D use_system_sqlite=0 \
	-D use_system_libxml=1 \
	-D use_system_zlib=1 \
	-D use_system_bzip2=1 \
	-D use_system_libpng=1 \
	-D use_system_libjpeg=1 \
	-D use_system_libevent=1 \
	-D use_system_flac=1 \
	-D use_system_vpx=0 \
	-D use_system_icu=0 \
%ifarch i586
	-D disable_sse2=1 \
	-D release_extra_cflags="-march=i586"
%endif
%ifarch armv7l
	-D target_arch=arm \
	-D disable_nacl=1 \
	-D linux_use_tcmalloc=0 \
	-D armv7=1 \
	-D release_extra_cflags="-marm"
%endif

# Note: DON'T use system sqlite (3.7.3) -- it breaks history search

%make chrome chrome_sandbox BUILDTYPE=Release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_crdir}/locales
mkdir -p %{buildroot}%{_crdir}/themes
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{_sourcedir}/chromium-wrapper %{buildroot}%{_crdir}/
install -m 755 out/Release/chrome %{buildroot}%{_crdir}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_crdir}/chrome-sandbox
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{crname}.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_crdir}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_crdir}/
%ifnarch armv7l
install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper %{buildroot}%{_crdir}/
install -m 644 out/Release/nacl_irt_*.nexe %{buildroot}%{_crdir}/
%endif
install -m 644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
install -m 755 out/Release/xdg-mime %{buildroot}%{_crdir}/
install -m 755 out/Release/xdg-settings %{buildroot}%{_crdir}/
install -m 644 out/Release/resources.pak %{buildroot}%{_crdir}/
ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{_sourcedir}/%{crname}.desktop %{buildroot}%{_datadir}/applications/

# icon
for i in 16 22 24 32 48 64 128 256; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
		%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/%{crname}.png
done

%clean
rm -rf %{buildroot}

%files -n chromium-browser

%files
%defattr(-,root,root,-)
%{_bindir}/%{crname}
%{_crdir}/chromium-wrapper
%{_crdir}/chrome
%{_crdir}/chrome-sandbox
%{_crdir}/chrome.pak
%{_crdir}/libffmpegsumo.so
%ifnarch armv7l
%{_crdir}/libppGoogleNaClPluginChrome.so
%{_crdir}/nacl_helper_bootstrap
%{_crdir}/nacl_helper
%{_crdir}/nacl_irt_*.nexe
%endif
%{_crdir}/locales
%{_crdir}/resources.pak
%{_crdir}/resources
%{_crdir}/themes
%{_crdir}/xdg-mime
%{_crdir}/xdg-settings
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.png
