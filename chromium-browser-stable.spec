# eol 'fix' corrupts some .bin files
%define dont_fix_eol 1

#define v8_ver 3.12.8
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define _src %{_topdir}/SOURCES
# Valid current basever numbers can be found at
# http://omahaproxy.appspot.com/
%define basever 56.0.2924.87
%define	debug_package %nil

%ifarch %ix86
%define _build_pkgcheck_set %{nil}
%endif

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys
# OpenMandriva key, id and secret
# For your own builds, please get your own set of keys.
%define    google_api_key AIzaSyAraWnKIFrlXznuwvd3gI-gqTozL-H-8MU
%define    google_default_client_id 1089316189405-m0ropn3qa4p1phesfvi2urs7qps1d79o.apps.googleusercontent.com
%define    google_default_client_secret RDdr-pHq2gStY4uw0m-zxXeo

%bcond_with	plf
# Always support proprietary codecs
# or html5 does not work
%if %{with plf}
%define extrarelsuffix plf
%define distsuffix plf
%endif

Name: 		chromium-browser-stable
Version: 	%basever
Release: 	1%{?extrarelsuffix}
Summary: 	A fast webkit-based web browser
Group: 		Networking/WWW
License: 	BSD, LGPL
# From : http://gsdview.appspot.com/chromium-browser-official/
Source0: 	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{basever}.tar.xz
Source1: 	chromium-wrapper
Source2: 	chromium-browser.desktop
Source3:	master_preferences

Patch0:         chromium-30.0.1599.66-master-prefs-path.patch
#Patch1:		chromium-36.0.1985.143-compile.patch
#Patch2:		chromium-fix-arm-sysroot.patch
#Patch3:		chromium-fix-arm-icu.patch
%if %mdvver >= 201500
# Don't use clang's integrated as while trying to check the version of gas
#Patch4:		chromium-36.0.1985.143-clang-no-integrated-as.patch
%endif
Patch5:		chromium-54.0.2840.100-dont-crash-with-glibc-2.24.patch

# PATCH-FIX-OPENSUSE patches in system glew library
#Patch13:        chromium-25.0.1364.172-system-glew.patch
# PATCH-FIX-OPENSUSE removes build part for courgette
#Patch14:        chromium-25.0.1364.172-no-courgette.patch
# PATCH-FIX-OPENSUSE Compile the sandbox with -fPIE settings
#Patch15:        chromium-25.0.1364.172-sandbox-pie.patch

# Debian Patches
#Patch17:	arm.patch
#Patch18:	arm-neon.patch
#Patch19:	fix-ld-on-arm.patch

Patch20:	chromium-last-commit-position-r0.patch

Provides: 	%{crname}
Obsoletes: 	chromium-browser-unstable < 26.0.1410.51
Obsoletes: 	chromium-browser-beta < 26.0.1410.51
Obsoletes: 	chromium-browser < 1:9.0.597.94
BuildRequires: 	gperf
BuildRequires: 	bison
BuildRequires: 	flex
#BuildRequires: 	v8-devel
BuildRequires: 	alsa-oss-devel
%if %mdvver >= 201500
BuildRequires:	atomic-devel
BuildRequires:	harfbuzz-devel
%else
BuildRequires:	%{_lib}atomic1
%endif
BuildRequires: 	icu-devel
BuildRequires: 	jsoncpp-devel
BuildRequires: 	pkgconfig(expat)
BuildRequires: 	pkgconfig(glib-2.0)
BuildRequires: 	pkgconfig(nss)
BuildRequires: 	bzip2-devel
BuildRequires: 	jpeg-devel
BuildRequires: 	pkgconfig(libpng)
BuildRequires:	gtk+3.0-devel
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
chromium-browser-dev package instead.

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
chromium-browser-dev package instead.

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

rm -rf third_party/binutils/

echo "%{revision}" > build/LASTCHANGE.in

# Hard code extra version
FILE=chrome/common/channel_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

# gn is rather convoluted and not python3 friendly -- let's make
# sure it sees python2 when it calls python
ln -s %{_bindir}/python2 python

# Remove most bundled libraries. Some are still needed.
#build/linux/unbundle/remove_bundled_libraries.py \
#	third_party/libwebp \
#	third_party/libjpeg \
#	third_party/libusb \
#	third_party/libudev \
#	third_party/opus \
#	third_party/webrtc \
#	--do-remove

# workaround build failure
touch chrome/test/data/webui/i18n_process_css_test.html

%build
%ifarch %{arm}
# Use linker flags to reduce memory consumption on low-mem architectures
%global optflags %(echo %{optflags} | sed -e 's/-g /-g0 /' -e 's/-gdwarf-4//')
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH
# Use linker flags to reduce memory consumption
%global ldflags %{ldflags} -fuse-ld=bfd -Wl,--no-keep-memory -Wl,--reduce-memory-overheads
%endif

%if %mdvver >= 201500
%ifarch %arm
export CC=gcc
export CXX=g++
%else
export CC=clang
export CXX=clang++
%endif
%else
export CC=gcc
export CXX=g++
%endif

# gn is rather convoluted and not python3 friendly -- let's make
# sure it sees python2 when it calls python
export PATH=`pwd`:$PATH

myconf_gn=" use_sysroot=false is_debug=false use_gold=true"
%if %mdvver >= 201500
%ifarch %arm
myconf_gn+=" is_clang=false"
%else
myconf_gn+=" is_clang=true clang_base_path=\"/usr\" clang_use_chrome_plugins=false"
%endif
%else
myconf_gn+=" is_clang=false"
%endif

myconf_gn+=" treat_warnings_as_errors=false"
myconf_gn+=" use_system_libjpeg=true "
%if %mdvver >= 201500
#myconf_gn+=" use_system_harfbuzz=true "
%endif
myconf_gn+=" use_gnome_keyring=false "
myconf_gn+=" fatal_linker_warnings=false "
myconf_gn+=" system_libdir=\"%{_lib}\""
myconf_gn+=" use_allocator=\"none\""
myconf_gn+=" use_aura=true "
myconf_gn+=" use_gconf=false"
myconf_gn+=" use_gtk3=true "
myconf_gn+=" enable_nacl=false "
%if %{with plf}
myconf_gn+=" proprietary_codecs=true "
myconf_gn+=" ffmpeg_branding=\"Chrome\" "
%else
myconf_gn+=" proprietary_codecs=false"
%endif
%ifarch i586
myconf_gn+=" target_cpu=\"x86\""
%endif
%ifarch x86_64
myconf_gn+=" target_cpu=\"x64\""
%endif
%ifarch %arm
myconf_gn+=" target_cpi=\"arm\""
myconf_gn+=" remove_webcore_debug_symbols=true"
myconf_gn+=" rtc_build_with_neon=true"
%endif
myconf_gn+=" google_api_key=\"%{google_api_key}\""
myconf_gn+=" google_default_client_id=\"%{google_default_client_id}\""
myconf_gn+=" google_default_client_secret=\"%{google_default_client_secret}\""

python2 tools/gn/bootstrap/bootstrap.py -v --gn-gen-args "${myconf_gn}"

out/Release/gn gen --args="${myconf_gn}" out/Release

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
install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/%{name}/locales/
install -m 644 out/Release/chrome_100_percent.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/icudtl.dat %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/*.bin %{buildroot}%{_libdir}/%{name}/
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
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/chromium-wrapper
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/chrome-sandbox
%{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/chrome_100_percent.pak
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
