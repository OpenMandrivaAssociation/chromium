%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}

Summary:	A fast webkit-based web browser
Name:		chromium-browser-stable
Version:	27.0.1453.93
Release:	3
Group:		Networking/WWW
License:	BSD, LGPL
Source0:	http://download.rfremix.ru/storage/chromium/%{version}/chromium-%{version}.tar.xz
Source1:	chromium-wrapper
Source30:	master_preferences
Source2:	chromium-browser.desktop
Source100:	icons.tar.bz2
Patch0:		chromium-21.0.1171.0-remove-inline.patch
Patch1:		chromium-system-v8-r0.patch
Patch4:		chromium-26.0.1411.1-master-prefs-path.patch
ExclusiveArch:	%{ix86} x86_64 %{arm}

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gperf
BuildRequires:	yasm
BuildRequires:	bzip2-devel
BuildRequires:	cups-devel
BuildRequires:	elfutils-devel
BuildRequires:	jpeg-devel
BuildRequires:	pam-devel
BuildRequires:	icu-devel
BuildRequires:	speech-dispatcher-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  v8-devel
Provides:	%{crname}
Conflicts:	chromium-browser-unstable
Conflicts:	chromium-browser-beta
Obsoletes:	chromium-browser < 1:9.0.597.94

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

%package -n	chromium-browser
Summary:	A fast webkit-based web browser (transition package)
Epoch:		1
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}

%description -n	chromium-browser
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is a transition package that installs the stable channel Chromium
browser. If you prefer the dev channel browser, install the
chromium-browser-unstable package instead.

%prep
%setup -qn chromium-%{version}
%apply_patches

# Hard code extra version
FILE=chrome/common/chrome_version_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1
# bundled v8 go away
find v8 -type f \! -iname '*.gyp*' -delete || die

%build
%ifarch %{ix86}
# FIXME: gold linker dies with internal error in convert_types, at ../../gold/gold.h:192 on i586
export CC="%{__cc} -fuse-ld=bfd"
export CXX="%{__cxx} -fuse-ld=bfd"
mkdir -p BFD
ln -sf /usr/bin/ld.bfd BFD/ld
export PATH=$PWD/BFD:$PATH
%endif

%ifarch %{arm}
%global optflags -marm %{optflags}
%endif
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
        -D linux_sandbox_path=%{_libdir}/%{name}/chrome-sandbox \
        -D linux_sandbox_chrome_path=%{_libdir}/%{name}/chrome \
        -D linux_link_gnome_keyring=0 \
        -D use_gconf=0 \
        -D werror='' \
        -D use_system_sqlite=0 \
        -D use_system_libxml=0 \
        -D use_system_zlib=0 \
        -D use_system_bzip2=1 \
        -D use_system_libbz2=1 \
        -D use_system_libpng=0 \
        -D use_system_libjpeg=1 \
        -D use_system_libevent=1 \
        -D use_system_flac=1 \
        -D use_system_vpx=1 \
        -D use_system_speex=1 \
        -D use_system_libusb=1 \
        -D use_system_libexif=1 \
        -D use_system_libsrtp=1 \
        -D use_system_libmtp=1 \
        -D use_system_opus=1 \
        -D use_system_libwebp=1 \
        -D use_system_harfbuzz=1 \
        -D use_system_minizip=1 \
        -D use_system_yasm=1 \
        -D use_system_xdg_utils=1 \
        -D build_ffmpegsumo=1 \
        -D use_system_ffmpeg=0 \
        -D use_pulseaudio=1 \
        -D use_system_v8=1 \
        -D linux_link_libpci=1 \
        -D linux_link_gsettings=1 \
        -D linux_link_libspeechd=1 \
        -D linux_link_kerberos=1 \
        -D linux_link_libgps=1 \
        -D use_system_icu=1 \
%ifarch i686
        -D disable_sse2=1 \
        -D release_extra_cflags="-march=i686"
%endif
%ifarch armv7l
        -D target_arch=arm \
        -D linux_use_tcmalloc=0 \
        -D disable_nacl=1 \
        -D armv7=1 \
        -D release_extra_cflags="-marm"
%endif

# Note: DON'T use system sqlite (3.7.3) -- it breaks history search

%make chrome chrome_sandbox BUILDTYPE=Release

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_crdir}/locales
mkdir -p %{buildroot}%{_crdir}/themes
mkdir -p %{buildroot}%{_crdir}/default_apps
install -m755 %{SOURCE1} -D %{buildroot}%{_crdir}/chromium-wrapper
install -m755 out/Release/chrome %{buildroot}%{_crdir}/
install -m4755 out/Release/chrome_sandbox %{buildroot}%{_crdir}/chrome-sandbox
install -m644 out/Release/chrome.1 -D %{buildroot}%{_mandir}/man1/%{crname}.1
install -m644 out/Release/chrome.pak %{buildroot}%{_crdir}/

install -m644 out/Release/chrome_100_percent.pak %{buildroot}%{_crdir}/
install -m644 out/Release/content_resources.pak %{buildroot}%{_crdir}/
install -m755 out/Release/libffmpegsumo.so %{buildroot}%{_crdir}/
%ifnarch %{arm}
install -m755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
install -m755 out/Release/nacl_helper_bootstrap %{buildroot}%{_crdir}/
install -m755 out/Release/nacl_helper %{buildroot}%{_crdir}/
install -m644 out/Release/nacl_irt_*.nexe %{buildroot}%{_crdir}/
%endif
install -m644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
#install -m755 out/Release/xdg-mime %{buildroot}%{_crdir}/
#install -m755 out/Release/xdg-settings %{buildroot}%{_crdir}/
install -m644 out/Release/resources.pak %{buildroot}%{_crdir}/
install -m644 chrome/browser/resources/default_apps/* %{buildroot}%{_crdir}/default_apps/
ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# Strip NaCl IRT
%ifarch x86_64
./native_client/toolchain/linux_x86_newlib/bin/x86_64-nacl-strip %{buildroot}%{_crdir}/nacl_irt_x86_64.nexe
%endif
%ifarch %{ix86}
./native_client/toolchain/linux_x86_newlib/bin/i686-nacl-strip %{buildroot}%{_crdir}/nacl_irt_x86_32.nexe
%endif

# desktop file
install -m644 %{SOURCE2} -D %{buildroot}%{_datadir}/applications/%{crname}.desktop

# icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/
tar xjf %{SOURCE100} -C %{buildroot}%{_iconsdir}/hicolor/

install -m644 %{SOURCE30} -D %{buildroot}%{_sysconfdir}/%{crname}/master_preferences
ln -s %{_datadir}/mdk/bookmarks/mozilla/mozilla-download.html %{buildroot}%{_sysconfdir}/%{crname}/default_bookmarks.html

find %{buildroot} -name "*.nexe" -exec strip {} \;

%files -n chromium-browser

%files
%config %{_sysconfdir}/%{crname}
%{_bindir}/%{crname}
%{_crdir}/chromium-wrapper
%{_crdir}/chrome
%{_crdir}/chrome-sandbox
%{_crdir}/chrome.pak
%{_crdir}/libffmpegsumo.so
%ifnarch %{arm}
%{_crdir}/libppGoogleNaClPluginChrome.so
%{_crdir}/nacl_helper_bootstrap
%{_crdir}/nacl_helper
%{_crdir}/nacl_irt_*.nexe
%endif
%{_crdir}/locales
%{_crdir}/resources.pak
%{_crdir}/resources
%{_crdir}/chrome_100_percent.pak
%{_crdir}/content_resources.pak
%{_crdir}/themes
%{_crdir}/default_apps
#%{_crdir}/xdg-mime
#%{_crdir}/xdg-settings
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.*

