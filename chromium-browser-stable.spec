%define revision 95650
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define basever 13.0.761.0
%define patchver() ([ -f %{_sourcedir}/patch-%1-%2.diff.xz ] || exit 1; xz -dc %{_sourcedir}/patch-%1-%2.diff.xz|patch -p1);

Name: chromium-browser-stable
Version: 13.0.782.112
Release: %mkrel 1
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL
Source0: chromium-%{basever}.tar.xz
Source1: chromium-wrapper
Source2: chromium-browser.desktop
Source1000: patch-13.0.761.0-13.0.767.1.diff.xz
Source1001: binary-13.0.761.0-13.0.767.1.tar.xz
Source1002: patch-13.0.767.1-13.0.772.0.diff.xz
Source1003: binary-13.0.767.1-13.0.772.0.tar.xz
Source1004: patch-13.0.772.0-13.0.782.1.diff.xz
Source1005: binary-13.0.772.0-13.0.782.1.tar.xz
Source1006: script-13.0.772.0-13.0.782.1.sh
Source1007: patch-13.0.782.1-13.0.782.11.diff.xz
Source1008: patch-13.0.782.11-13.0.782.13.diff.xz
Source1009: patch-13.0.782.13-13.0.782.15.diff.xz
Source1010: patch-13.0.782.15-13.0.782.20.diff.xz
Source1011: patch-13.0.782.20-13.0.782.24.diff.xz
Source1012: patch-13.0.782.24-13.0.782.32.diff.xz
Source1013: patch-13.0.782.32-13.0.782.41.diff.xz
Source1014: patch-13.0.782.41-13.0.782.99.diff.xz
Source1015: patch-13.0.782.99-13.0.782.107.diff.xz
Source1016: patch-13.0.782.107-13.0.782.112.diff.xz
Patch0: chromium-13.0.782.1-skip-builder-tests.patch
Patch1: chromium-13.0.767.1-gcc46.patch
Patch2: chromium-13.0.782.1-exclude-chromeos-options.patch
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
BuildRequires: libevent-devel libflac-devel
ExclusiveArch: i586 x86_64 armel

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
%patchver 13.0.761.0 13.0.767.1
tar xvf %{_sourcedir}/binary-13.0.761.0-13.0.767.1.tar.xz
%patchver 13.0.767.1 13.0.772.0
tar xvf %{_sourcedir}/binary-13.0.767.1-13.0.772.0.tar.xz
rm third_party/libsrtp/src/doc/libsrtp.pdf
%patchver 13.0.772.0 13.0.782.1
tar xvf %{_sourcedir}/binary-13.0.772.0-13.0.782.1.tar.xz
sh %{_sourcedir}/script-13.0.772.0-13.0.782.1.sh
%patchver 13.0.782.1 13.0.782.11
%patchver 13.0.782.11 13.0.782.13
%patchver 13.0.782.13 13.0.782.15
%patchver 13.0.782.15 13.0.782.20
%patchver 13.0.782.20 13.0.782.24
%patchver 13.0.782.24 13.0.782.32
%patchver 13.0.782.32 13.0.782.41
%patchver 13.0.782.41 13.0.782.99
%patchver 13.0.782.99 13.0.782.107
%patchver 13.0.782.107 13.0.782.112

%patch0 -p1 -b .skip-builder-tests
%patch1 -p1 -b .gcc46
%patch2 -p1 -b .exclude-chromeos-options
echo "%{revision}" > build/LASTCHANGE.in

sed -i -e '/test_support_common/s/^/#/' \
	chrome/browser/sync/tools/sync_tools.gyp

# Hard code extra version
FILE=chrome/browser/platform_util_common_linux.cc
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
install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
install -m 644 out/Release/xdg-settings %{buildroot}%{_crdir}/
install -m 644 out/Release/resources.pak %{buildroot}%{_crdir}/
ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{_sourcedir}/%{crname}.desktop %{buildroot}%{_datadir}/applications/

# icon
for i in 16 32 48 256; do
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
%{_crdir}/libppGoogleNaClPluginChrome.so
%{_crdir}/locales
%{_crdir}/resources.pak
%{_crdir}/resources
%{_crdir}/themes
%{_crdir}/xdg-settings
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.png
