%define revision 213526
#define v8_ver 3.12.8
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define _src %{_topdir}/SOURCES
%define basever 29.0.1547.65
#define	debug_package %nil

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys
# OpenMandriva key, id and secret
# For your own builds, please get your own set of keys.
%define    google_api_key AIzaSyAwh8uqAFaEtP0j3J6OP0Z3fhVCYUBcyxM
%define    google_default_client_id 487576112834.apps.googleusercontent.com
%define    google_default_client_secret G5nOV_TkIemhoYAZ8mchGpTi

%bcond_with	plf
# Always support proprietary codecs
# or html5 does not work


Name: 		chromium-browser-stable
Version: 	%basever
Release: 	3
Summary: 	A fast webkit-based web browser
Group: 		Networking/WWW
License: 	BSD, LGPL
# From : http://gsdview.appspot.com/chromium-browser-official/
Source0: 	chromium-%{basever}.tar.xz
Source1: 	chromium-wrapper
Source2: 	chromium-browser.desktop
Source3:	master_preferences
Provides: 	%{crname}
Obsoletes: 	chromium-browser-unstable < 26.0.1410.51
Obsoletes: 	chromium-browser-beta < 26.0.1410.51
Obsoletes: 	chromium-browser < 1:9.0.597.94
BuildRequires: 	gperf
BuildRequires: 	bison
BuildRequires: 	flex
BuildRequires: 	alsa-oss-devel
BuildRequires: 	icu-devel
BuildRequires: 	jsoncpp-devel
BuildRequires: 	harfbuzz-devel
BuildRequires: 	v8-devel
BuildRequires: 	pkgconfig(expat)
BuildRequires: 	pkgconfig(glib-2.0)
BuildRequires: 	pkgconfig(nss)
BuildRequires: 	bzip2-devel
BuildRequires: 	jpeg-devel
BuildRequires: 	pkgconfig(libpng)
BuildRequires:	gtk+2.0-devel
BuildRequires: 	pkgconfig(nspr)
BuildRequires: 	pkgconfig(zlib)
BuildRequires: 	pkgconfig(xscrnsaver)
BuildRequires: 	pkgconfig(glu)
BuildRequires: 	pkgconfig(gl)
BuildRequires: 	cups-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires: 	pkgconfig(gnome-keyring-1)
BuildRequires: 	pam-devel
BuildRequires: 	pkgconfig(vpx)
BuildRequires: 	pkgconfig(xtst)
BuildRequires: 	pkgconfig(libxslt)
BuildRequires: 	pkgconfig(libxml-2.0)
BuildRequires: 	pkgconfig(libpulse)
BuildRequires: 	pkgconfig(xt)
BuildRequires: 	elfutils-devel
BuildRequires: 	pkgconfig(gnutls)
BuildRequires: 	pkgconfig(libevent)
BuildRequires: 	pkgconfig(udev)
BuildRequires: 	pkgconfig(flac)
BuildRequires: 	pkgconfig(opus)
BuildRequires: 	pkgconfig(libwebp)
BuildRequires: 	pkgconfig(speex)
BuildRequires: 	pkgconfig(minizip)
BuildRequires:  pkgconfig(protobuf)
BuildRequires: 	yasm
BuildRequires: 	pkgconfig(libusb-1.0)
BuildRequires:  speech-dispatcher-devel
BuildRequires:  pkgconfig(libpci)

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-browser-unstable package instead.

%package -n chromium-browser
Summary: 	A fast webkit-based web browser (transition package)
Epoch: 		1
Group:		Networking/WWW
Requires: 	%{name} = %{version}-%{release}

%description -n chromium-browser
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is a transition package that installs the stable channel Chromium
browser. If you prefer the dev channel browser, install the
chromium-browser-unstable package instead.

%prep
%setup -q -n chromium-%{basever}

echo "%{revision}" > build/LASTCHANGE.in

# Hard code extra version
FILE=chrome/common/chrome_version_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

%build
%ifarch %{ix86}
%define optflags %(echo %{optflags} | sed 's/-g//')
%endif
#
# We need to find why even if building w -Duse_system_libpng=0, this is built with third party libpng.
# We able bundle one in stable release for now and will work on beta with system libpng
#
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
        -Dlinux_sandbox_path=%{_crdir}/chrome-sandbox \
        -Dlinux_sandbox_chrome_path=%{_crdir}/chrome \
        -Dlinux_link_gnome_keyring=0 \
	-Dlinux_link_gsettings=1 \
	-Dlinux_link_libpci=1 \
	-Dlinux_link_libspeechd=1 \
        -Duse_gconf=0 \
        -Dwerror='' \
        -Duse_system_sqlite=0 \
        -Duse_system_libxml=1 \
        -Duse_system_zlib=1 \
        -Duse_system_bzip2=1 \
	-Duse_system_jsoncpp=1 \
        -Duse_system_xdg_utils=1 \
        -Duse_system_libpng=1 \
        -Duse_system_libjpeg=1 \
	-Duse_system_harfbuzz=1 \
        -Duse_system_libevent=1 \
	-Ddisable_newlib_untar=1 \
	-Duse_system_yasm=1 \
	-Duse_system_libwebp=1 \
	-Duse_system_opus=1 \
        -Duse_system_flac=1 \
        -Duse_system_vpx=1 \
        -Duse_system_icu=1 \
	-Duse_system_nspr=1 \
        -Duse_system_libusb=1 \
        -Dlinux_use_tcmalloc=0 \
	-Duse_system_minizip=1 \
	-Duse_system_protobuf=1 \
	-Ddisable_nacl=1 \
        -Ddisable_sse2=1 \
	-Duse_pulseaudio=1 \
        -Duse_system_v8=1 \
	-Dlinux_use_gold_binary=0 \
	-Dlinux_use_gold_flags=0 \
%if %{with plf}
	-Dproprietary_codecs=1 \
	-Dffmpeg_branding=Chrome \
%else
	-Dproprietary_codecs=1 \
%endif
        -Duse_system_speex=1 \
%ifarch i586
	-Dtarget_arch=ia32 \
        -Drelease_extra_cflags="%optflags -march=i586" \
%endif
%ifarch x86_64
	-Dtarget_arch=x64 \
        -Drelease_extra_cflags="%optflags" \
%endif
%ifarch armv7hl
	-Darm_float_abi=hard \
	-Dv8_use_arm_eabi_hardfloat=true \
        -Drelease_extra_cflags="%optflags -DUSE_EABI_HARDFLOAT" \
%endif
%ifarch %arm
	-Darm_fpu=vfpv3-d16 \
	-Darmv7=1 \
%endif
        -Dgoogle_api_key=%{google_api_key} \
        -Dgoogle_default_client_id=%{google_default_client_id} \
        -Dgoogle_default_client_secret=%{google_default_client_secret} \
# Note: DON'T use system sqlite (3.7.3) -- it breaks history search
%make chrome chrome_sandbox chromedriver BUILDTYPE=Release

%install
ls out/Release
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_crdir}/locales
mkdir -p %{buildroot}%{_crdir}/themes
mkdir -p %{buildroot}%{_crdir}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{SOURCE1} %{buildroot}%{_crdir}/
install -m 755 out/Release/chrome %{buildroot}%{_crdir}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_crdir}/chrome-sandbox
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{crname}.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_crdir}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_crdir}/
#install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
#install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{_crdir}/
#install -m 755 out/Release/nacl_helper %{buildroot}%{_crdir}/
#install -m 644 out/Release/nacl_irt_*.nexe %{buildroot}%{_crdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
install -m 644 out/Release/resources.pak %{buildroot}%{_crdir}/
install -m 644 out/Release/content_resources.pak %{buildroot}%{_crdir}/
#install -m 644 out/Release/theme_resources_standard.pak %{buildroot}%{_crdir}/
#install -m 644 out/Release/ui_resources_standard.pak %{buildroot}%{_crdir}/
install -m 644 out/Release/chrome_100_percent.pak %{buildroot}%{_crdir}/
install -m 644 out/Release/chrome_remote_desktop.pak %{buildroot}%{_crdir}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_crdir}/default_apps/

ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# Strip NaCl IRT
#./native_client/toolchain/linux_x86_newlib/bin/x86_64-nacl-strip --strip-debug %{buildroot}%{_crdir}/nacl_irt_x86_64.nexe
#./native_client/toolchain/linux_x86_newlib/bin/i686-nacl-strip --strip-debug %{buildroot}%{_crdir}/nacl_irt_x86_32.nexe

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m644 %{SOURCE2} %{buildroot}%{_datadir}/applications/
install -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/%{crname}/master_preferences

# icon
for i in 22 24 48 64 128 256; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
		%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/%{crname}.png
done

for i in 16 26 32; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/default_100_percent/chromium/product_logo_$i.png \
		%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/%{crname}.png
done

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
#%{_crdir}/libppGoogleNaClPluginChrome.so
#%{_crdir}/nacl_helper_bootstrap
#%{_crdir}/nacl_helper
#%{_crdir}/nacl_irt_*.nexe
%{_crdir}/locales
%{_crdir}/content_resources.pak
#%{_crdir}/theme_resources_standard.pak
#%{_crdir}/ui_resources_standard.pak
%{_crdir}/chrome_remote_desktop.pak
%{_crdir}/chrome_100_percent.pak
%{_crdir}/resources.pak
%{_crdir}/resources
%{_crdir}/themes
%{_crdir}/default_apps
%{_mandir}/man1/%{crname}*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{crname}.png
