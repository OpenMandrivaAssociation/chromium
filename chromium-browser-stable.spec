#define v8_ver 3.12.8
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define _src %{_topdir}/SOURCES
# Valid current basever numbers can be found at
# http://omahaproxy.appspot.com/
%define basever 37.0.2062.120
%define	debug_package %nil

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
Source0: 	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{basever}.tar.xz
Source1: 	chromium-wrapper
Source2: 	chromium-browser.desktop
Source3:	master_preferences

Patch0:         chromium-30.0.1599.66-master-prefs-path.patch
Patch1:		chromium-36.0.1985.143-compile.patch
#Patch2:		chromium-fix-arm-sysroot.patch
Patch3:		chromium-fix-arm-icu.patch
%if %mdvver >= 201500
# Don't use clang's integrated as while trying to check the version of gas
Patch4:		chromium-36.0.1985.143-clang-no-integrated-as.patch
%endif

# PATCH-FIX-OPENSUSE patches in system glew library
Patch13:        chromium-25.0.1364.172-system-glew.patch
# PATCH-FIX-OPENSUSE removes build part for courgette
Patch14:        chromium-25.0.1364.172-no-courgette.patch
# PATCH-FIX-OPENSUSE Compile the sandbox with -fPIE settings
Patch15:        chromium-25.0.1364.172-sandbox-pie.patch

# Debian Patches
Patch16:	arm-neon.patch
Patch17:	arm.patch
Patch19:	fix-ld-on-arm.patch

Provides: 	%{crname}
Obsoletes: 	chromium-browser-unstable < 26.0.1410.51
Obsoletes: 	chromium-browser-beta < 26.0.1410.51
Obsoletes: 	chromium-browser < 1:9.0.597.94
BuildRequires: 	gperf
BuildRequires: 	bison
BuildRequires: 	flex
#BuildRequires: 	v8-devel
BuildRequires: 	alsa-oss-devel
BuildRequires: 	icu-devel
BuildRequires: 	jsoncpp-devel
BuildRequires: 	harfbuzz-devel
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
BuildRequires: 	cap-devel
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
BuildRequires:	pkgconfig(libexif)
%if %mdvver >= 201500
BuildRequires:	python2
%else
BuildRequires:	python
%endif
BuildRequires:	ninja

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

%package -n chromedriver
Summary:        WebDriver for Google Chrome/Chromium
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}


%description -n chromedriver
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.


%prep
%setup -q -n chromium-%{basever}
%apply_patches

echo "%{revision}" > build/LASTCHANGE.in

# Hard code extra version
FILE=chrome/common/chrome_version_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

# remove bundle v8
#find v8 -type f \! -iname '*.gyp*' -delete
#build/linux/unbundle/replace_gyp_files.py
#-Duse_system_v8=1 \

# gyp is rather convoluted and not python3 friendly -- let's make
# sure it sees python2 when it calls python
ln -s %{_bindir}/python2 python

%build
# gyp is rather convoluted and not python3 friendly -- let's make
# sure it sees python2 when it calls python
export PATH=`pwd`:$PATH

# We need to find why even if building w -Duse_system_libpng=0, this is built with third party libpng.
# We able bundle one in stable release for now and will work on beta with system libpng
#
export GYP_GENERATORS=ninja
build/gyp_chromium --depth=. \
        -Dlinux_sandbox_path=%{_crdir}/chrome-sandbox \
        -Dlinux_sandbox_chrome_path=%{_crdir}/chrome \
        -Dlinux_link_gnome_keyring=0 \
	-Dlinux_link_gsettings=1 \
	-Dlinux_link_libpci=1 \
	-Dlinux_link_libspeechd=1 \
        -Duse_gconf=0 \
        -Dwerror='' \
	-Ddisable_fatal_linker_warnings=1 \
	-Dsystem_libdir=%{_lib} \
	-Dpython_ver=%{python_version} \
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
        -Duse_system_icu=0 \
	-Duse_system_nspr=1 \
        -Duse_system_libusb=1 \
        -Duse_allocator=none \
	-Duse_system_minizip=1 \
	-Duse_system_protobuf=0 \
	-Ddisable_nacl=1 \
        -Ddisable_sse2=1 \
	-Duse_pulseaudio=1 \
	-Dlinux_use_gold_binary=1 \
	-Dlinux_use_gold_flags=1 \
%if %{with plf}
	-Dproprietary_codecs=1 \
	-Dffmpeg_branding=Chrome \
%else
	-Dproprietary_codecs=1 \
%endif
        -Duse_system_speex=1 \
%ifarch i586
	-Dtarget_arch=ia32 \
%endif
%ifarch x86_64
	-Dtarget_arch=x64 \
%endif
%ifarch armv7hl
	-Darm_float_abi=hard \
	-Dv8_use_arm_eabi_hardfloat=true \
	-Drelease_extra_cflags="%optflags -DUSE_EABI_HARDFLOAT" \
%endif
%ifarch %arm
	-Darm_fpu=vfpv3-d16 \
	-Darm_thumb=1 \
	-Darm_neon_optional=0 \
	-Dremove_webcore_debug_symbols=1 \
	-Darm_neon=0 \
	-Darmv7=1 \
%endif
        -Dgoogle_api_key=%{google_api_key} \
        -Dgoogle_default_client_id=%{google_default_client_id} \
        -Dgoogle_default_client_secret=%{google_default_client_secret}
# Note: DON'T use system sqlite (3.7.3) -- it breaks history search
# As of 36.0.1985.143, use_system_icu breaks the build.
# gyp: Duplicate target definitions for /home/bero/abf/chromium-browser-stable/BUILD/chromium-36.0.1985.143/third_party/icu/icu.gyp:icudata#target
# This should be enabled again once the gyp files are fixed.
ninja -C out/Release chrome chrome_sandbox chromedriver

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}/locales
mkdir -p %{buildroot}%{_libdir}/%{name}/themes
mkdir -p %{buildroot}%{_libdir}/%{name}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{SOURCE1} %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/chrome %{buildroot}%{_libdir}/%{name}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_libdir}/%{name}/chrome-sandbox
cp -a out/Release/chromedriver %{buildroot}%{_libdir}/%{name}/chromedriver
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/%{name}/locales/
install -m 644 out/Release/chrome_100_percent.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/content_resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/icudtl.dat %{buildroot}%{_libdir}/%{name}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_libdir}/%{name}/default_apps/
ln -s %{_libdir}/%{name}/chromium-wrapper %{buildroot}%{_bindir}/%{name}
ln -s %{_libdir}/%{name}/chromedriver %{buildroot}%{_bindir}/chromedriver

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_libdir}/%{name}

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applications/

# icon
for i in 22 24 48 64 128 256; do
        mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
        install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
                %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install the master_preferences file
mkdir -p %{buildroot}%{_sysconfdir}/chromium
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/chromium


find %{buildroot} -name "*.nexe" -exec strip {} \;

%files -n chromium-browser

%files
%doc LICENSE AUTHORS
%config %{_sysconfdir}/chromium
%{_bindir}/%{name}
%{_libdir}/%{name}/chromium-wrapper
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/chrome-sandbox
%{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/libffmpegsumo.so
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/chrome_100_percent.pak
%{_libdir}/%{name}/content_resources.pak
%{_libdir}/%{name}/resources.pak
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/themes
%{_libdir}/%{name}/default_apps
%{_mandir}/man1/%{name}*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%files -n chromedriver
%doc LICENSE AUTHORS
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver
