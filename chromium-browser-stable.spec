%define channel stable
%if "%{channel}" == "stable"
%define namesuffix %{nil}
%else
%define namesuffix -%{channel}
%endif

%define _disable_ld_no_undefined 1
# Chromium buildmess uses its own LTO
%global _disable_lto 1

# eol 'fix' corrupts some .bin files
%define dont_fix_eol 1

#define v8_ver 3.12.8
%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define _src %{_topdir}/SOURCES
%define	debug_package %nil

%ifarch %ix86
%define _build_pkgcheck_set %{nil}
%endif

# Libraries that should be unbundled
%global system_libs icu fontconfig harfbuzz-ng libjpeg libpng snappy libdrm ffmpeg flac libwebp zlib libxml libxslt re2 libusb libevent freetype opus freetype opus openh264
# FIXME add libvpx

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys
# OpenMandriva key, id and secret
# For your own builds, please get your own set of keys.
%define    google_api_key AIzaSyAraWnKIFrlXznuwvd3gI-gqTozL-H-8MU
%define    google_default_client_id 1089316189405-m0ropn3qa4p1phesfvi2urs7qps1d79o.apps.googleusercontent.com
%define    google_default_client_secret RDdr-pHq2gStY4uw0m-zxXeo

%bcond_with	plf
# crisb - ozone causes a segfault on startup as of 57.0.2987.133, doesn't compile in 80.x
%bcond_with	ozone
# Breaks the build as of chromium 83, icu 66.1
%bcond_without	system_icu
%bcond_without	system_ffmpeg
# Temporarily broken, cr_z_* symbols used even when we're supposed to use system minizip
%bcond_without	system_minizip
# chromium 58 fails with system vpx 1.6.1
%bcond_without	system_vpx
# system re2 doesn't work with custom libcxx
%bcond_without	system_re2

# Always support proprietary codecs
# or html5 does not work
%if %{with plf}
%define extrarelsuffix plf
%define distsuffix plf
%endif

Name: 		chromium-browser-%{channel}
# Working version numbers can be found at
# http://omahaproxy.appspot.com/
Version: 	90.0.4430.72
Release: 	1%{?extrarelsuffix}
Summary: 	A fast webkit-based web browser
Group: 		Networking/WWW
License: 	BSD, LGPL
# From : http://gsdview.appspot.com/chromium-browser-official/
Source0: 	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
Source1: 	chromium-wrapper
Source2: 	chromium-browser%{namesuffix}.desktop
Source3:	master_preferences
# https://bugs.freedesktop.org/show_bug.cgi?id=106490
# Workaround from Arch Linux
# https://aur.archlinux.org/cgit/aur.git/tree/chromium-drirc-disable-10bpc-color-configs.conf?h=chromium-vaapi
Source4:	chromium-drirc-disable-10bpc-color-configs.conf
Source100:	%{name}.rpmlintrc

### Chromium Fedora Patches ###
Patch0:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-70.0.3538.67-sandbox-pie.patch
# Use /etc/chromium for master_prefs
Patch1:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-68.0.3440.106-master-prefs-path.patch
# Use gn system files
Patch2:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-67.0.3396.62-gn-system.patch
# Do not prefix libpng functions
Patch4:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-60.0.3112.78-no-libpng-prefix.patch
# Do not mangle zlib
Patch6:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-77.0.3865.75-no-zlib-mangle.patch
# Use Gentoo's Widevine hack
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-widevine-r3.patch
Patch8:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-71.0.3578.98-widevine-r3.patch
# Disable fontconfig cache magic that breaks remoting (originally from Fedora, ported to 81 code base)
Patch9:		chromium-83-disable-fontconfig-cache-magic.patch
# drop rsp clobber, which breaks gcc9 (thanks to Jeff Law)
Patch10:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-78.0.3904.70-gcc9-drop-rsp-clobber.patch
# Try to load widevine from other places
Patch11:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-widevine-other-locations.patch
# Try to fix version.py for Rawhide
Patch12:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-71.0.3578.98-py2-bootstrap.patch
# Add "Fedora" to the user agent string
#Patch13:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-fedora-user-agent.patch
# Needs to be submitted..
Patch51:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-76.0.3809.100-gcc-remoting-constexpr.patch
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-unbundle-zlib.patch
Patch53:	chromium-81-unbundle-zlib.patch
# Needs to be submitted..
Patch54:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-77.0.3865.75-gcc-include-memory.patch
# /../../ui/base/cursor/ozone/bitmap_cursor_factory_ozone.cc:53:15: error: 'find_if' is not a member of 'std'; did you mean 'find'? 
#Patch63:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-fix-find_if.patch


# Use lstdc++ on EPEL7 only
#Patch101:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-75.0.3770.100-epel7-stdc++.patch
# el7 only patch
#Patch102:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-el7-noexcept.patch

# Apply these patches to work around EPEL8 issues
#Patch300:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-76.0.3809.132-rhel8-force-disable-use_gnome_keyring.patch

#Patch501:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-75.0.3770.80-SIOCGSTAMP.patch

### Chromium gcc/libstdc++ support ###
# https://github.com/stha09/chromium-patches
Patch550:	https://raw.githubusercontent.com/stha09/chromium-patches/master/chromium-86-ConsumeDurationNumber-constexpr.patch
Patch551:	https://raw.githubusercontent.com/stha09/chromium-patches/master/chromium-86-ImageMemoryBarrierData-init.patch
Patch553:	https://raw.githubusercontent.com/stha09/chromium-patches/master/chromium-87-compiler.patch
Patch554:	https://raw.githubusercontent.com/stha09/chromium-patches/master/chromium-86-nearby-explicit.patch
Patch555:	https://raw.githubusercontent.com/stha09/chromium-patches/master/chromium-86-nearby-include.patch
Patch557:	https://raw.githubusercontent.com/stha09/chromium-patches/master/chromium-78-protobuf-RepeatedPtrField-export.patch
Patch559:	https://raw.githubusercontent.com/stha09/chromium-patches/master/chromium-80-QuicStreamSendBuffer-deleted-move-constructor.patch
Patch560:	https://raw.githubusercontent.com/stha09/chromium-patches/master/chromium-84-blink-disable-clang-format.patch

### Chromium Tests Patches ###
# suse, system libs
Patch600:	arm_use_right_compiler.patch
# Arch Linux, fix for compile error with system ICU
Patch602:	https://raw.githubusercontent.com/archlinuxarm/PKGBUILDs/master/extra/chromium/chromium-system-icu.patch

# Enable VAAPI support on Linux
Patch650:	https://raw.githubusercontent.com/saiarcot895/chromium-ubuntu-build/master/debian/patches/enable-vaapi-on-linux.diff
Patch651:	https://raw.githubusercontent.com/saiarcot895/chromium-ubuntu-build/master/debian/patches/vdpau-support.patch
Patch652:	chromium-88-default-video-acceleration-on.patch

# Fixes from Arch
Patch660:	https://aur.archlinux.org/cgit/aur.git/plain/chromium-skia-harmony.patch
Patch661:	https://aur.archlinux.org/cgit/aur.git/plain/wayland-egl.patch
Patch662:	https://aur.archlinux.org/cgit/aur.git/plain/chromium-glibc-2.33.patch


# mga
Patch700:	chromium-81-extra-media.patch
Patch701:	chromium-69-wmvflvmpg.patch

# omv
Patch1001:	chromium-64-system-curl.patch
Patch1002:	chromium-69-no-static-libstdc++.patch
Patch1003:	chromium-system-zlib.patch
Patch1004:	chromium-88-less-blacklist-nonsense.patch
Patch1005:	chromium-90-compilefixes.patch
Patch1006:	chromium-90-buildfixes.patch
Patch1007:	chromium-81-enable-gpu-features.patch

Provides: 	%{crname}
Obsoletes: 	chromium-browser-unstable < 26.0.1410.51
Obsoletes: 	chromium-browser-beta < 26.0.1410.51
Obsoletes: 	chromium-browser < 1:9.0.597.94
BuildRequires: 	gperf
BuildRequires: 	bison
BuildRequires: 	re2c
BuildRequires: 	flex
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(krb5)
BuildRequires:	pkgconfig(openh264)
BuildRequires:	pkgconfig(libunwind)
%if %{with system_re2}
BuildRequires:	pkgconfig(re2)
%endif
BuildRequires:	pkgconfig(com_err)
BuildRequires:	python2dist(json5)
BuildRequires:	python2-pkg-resources
BuildRequires:	python2-xcbgen
BuildRequires: 	alsa-oss-devel
BuildRequires:	atomic-devel
BuildRequires:	harfbuzz-devel
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires: 	snappy-devel
BuildRequires: 	jsoncpp-devel
BuildRequires: 	pkgconfig(expat)
BuildRequires: 	pkgconfig(glib-2.0)
BuildRequires: 	pkgconfig(wayland-egl)
BuildRequires: 	pkgconfig(nss)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-glx)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:	pkgconfig(dri)
BuildRequires:	%{_lib}GL-devel
BuildRequires: 	bzip2-devel
BuildRequires: 	jpeg-devel
BuildRequires: 	pkgconfig(libpng)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	clang lld
%if %{with system_ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat) >= 57.41.100
BuildRequires:  pkgconfig(libavutil)
%endif
BuildRequires:	gtk+3.0-devel
BuildRequires:	gtk+2.0-devel
BuildRequires: 	pkgconfig(nspr)
BuildRequires: 	pkgconfig(zlib)
BuildRequires: 	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xshmfence)
BuildRequires: 	pkgconfig(glu)
BuildRequires: 	pkgconfig(gl)
BuildRequires: 	cups-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires: 	pkgconfig(gnome-keyring-1)
BuildRequires: 	pam-devel
%if %{with system_vpx}
BuildRequires: 	pkgconfig(vpx)
%endif
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
BuildRequires:	pkgconfig(lcms2)
%if %{with system_minizip}
BuildRequires: 	pkgconfig(minizip)
%endif
BuildRequires:  pkgconfig(protobuf)
BuildRequires: 	yasm
BuildRequires: 	pkgconfig(libusb-1.0)
BuildRequires:  speech-dispatcher-devel
BuildRequires:  pkgconfig(libpci)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	python2
BuildRequires:	ninja
BuildRequires:	nodejs
BuildRequires:	python2-markupsafe
BuildRequires:	python2-ply
BuildRequires:	python2-beautifulsoup4
BuildRequires:	python2-simplejson
BuildRequires:	python2-html5lib
BuildRequires:	jdk-current

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-browser-dev package instead.

%if "%{channel}" == "stable"
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
%endif

%package -n chromedriver%{namesuffix}
Summary:	WebDriver for Google Chrome/Chromium
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}


%description -n chromedriver%{namesuffix}
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.


%prep
%autosetup -p1 -n chromium-%{version}

rm -rf third_party/binutils/

echo "%{revision}" > build/LASTCHANGE.in

sed -i 's!-nostdlib++!!g'  build/config/posix/BUILD.gn
sed -i 's!ffmpeg_buildflags!ffmpeg_features!g' build/linux/unbundle/ffmpeg.gn
 
# Hard code extra version
FILE=chrome/common/channel_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

# gn is rather convoluted and not python3 friendly -- let's make
# sure it sees python2 when it calls python
ln -s %{_bindir}/python2 python

# use the system nodejs
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s /usr/bin/node third_party/node/linux/node-linux-x64/bin/

# Remove bundled libs
# We could use build/linux/unbundle/remove_bundled_libraries.py here, but
# that requires listing the (much bigger set of) remaining libraries and
# pulls in yet another python2 dep -- so let's use the trick found in the
# Arch PKGBUILD file instead
for lib in %{system_libs}; do
	# Fix mismatch between name and directory name
	[ "$lib" = "libjpeg" ] && lib="libjpeg_turbo"
	# libevent lives in base/third_party rather than third_party
	[ "$lib" = "libevent" ] && continue
	find "third_party/$lib" -type f \
		\! -path "third_party/$lib/chromium/*" \
		\! -path "third_party/$lib/google/*" \
		\! -path "third_party/harfbuzz-ng/utils/hb_scoped.h" \
		\! -regex '.*\.\(gn\|gni\|isolate\)' \
		-delete
done
python2 build/linux/unbundle/replace_gn_files.py \
	--system-libraries %{system_libs}

# Look, I don't know. This package is spit and chewing gum. Sorry.
rm -rf third_party/markupsafe
ln -s %{python2_sitearch}/markupsafe third_party/markupsafe
# We should look on removing other python packages as well i.e. ply

# workaround build failure
if [ ! -f chrome/test/data/webui/i18n_process_css_test.html ]; then
	touch chrome/test/data/webui/i18n_process_css_test.html
fi

%build
. %{_sysconfdir}/profile.d/90java.sh

%ifarch %{arm}
# Use linker flags to reduce memory consumption on low-mem architectures
%global optflags %(echo %{optflags} | sed -e 's/-g /-g0 /' -e 's/-gdwarf-4//')
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH
# Use linker flags to reduce memory consumption
%global ldflags %{ldflags} -fuse-ld=bfd -Wl,--no-keep-memory -Wl,--reduce-memory-overheads
%endif
%ifarch %{ix86}
# Workaround for build failure
%global ldflags %{ldflags} -Wl,-z,notext
%endif
%global optflags %{optflags} -I%{_includedir}/libunwind

export CC=clang
export CXX=clang++

# gn is rather convoluted and not python3 friendly -- let's make
# sure it sees python2 when it calls python
export PATH=`pwd`:$PATH

CHROMIUM_CORE_GN_DEFINES="use_sysroot=false is_debug=false fieldtrial_testing_like_official_build=true use_lld=false use_gold=true"
CHROMIUM_CORE_GN_DEFINES+=" is_clang=true clang_base_path=\"%{_prefix}\" clang_use_chrome_plugins=false "
CHROMIUM_CORE_GN_DEFINES+=" treat_warnings_as_errors=false "
CHROMIUM_CORE_GN_DEFINES+=" use_custom_libcxx=false "
for i in %{system_libs}; do
	[ "$i" = "harfbuzz-ng" ] && continue
	CHROMIUM_CORE_GN_DEFINES+=" use_system_$i=true "
done
CHROMIUM_CORE_GN_DEFINES+=" use_system_libjpeg=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_lcms2=true "
#CHROMIUM_CORE_GN_DEFINES+=" use_system_libpng=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_harfbuzz=true "
#CHROMIUM_CORE_GN_DEFINES+=" use_system_libdrm=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_minigbm=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_wayland=true "
CHROMIUM_CORE_GN_DEFINES+=" use_xkbcommon=true "
#CHROMIUM_CORE_GN_DEFINES+=" use_glib=false use_atk=false "
#CHROMIUM_CORE_GN_DEFINES+=" use_gtk=false "
%if %{with system_icu}
CHROMIUM_CORE_GN_DEFINES+=" use_system_icu=true "
%else
CHROMIUM_CORE_GN_DEFINES+=" icu_use_data_file=true"
%endif
CHROMIUM_CORE_GN_DEFINES+=" use_gnome_keyring=false "
CHROMIUM_CORE_GN_DEFINES+=" fatal_linker_warnings=false "
CHROMIUM_CORE_GN_DEFINES+=" system_libdir=\"%{_lib}\""
CHROMIUM_CORE_GN_DEFINES+=" use_allocator=\"none\""
CHROMIUM_CORE_GN_DEFINES+=" use_aura=true "
#CHROMIUM_CORE_GN_DEFINES+=" use_gio=true"
%if %{with ozone}
CHROMIUM_CORE_GN_DEFINES+=" use_ozone=true "
%endif
CHROMIUM_CORE_GN_DEFINES+=" enable_nacl=false "
CHROMIUM_CORE_GN_DEFINES+=" proprietary_codecs=true "
CHROMIUM_CORE_GN_DEFINES+=" ffmpeg_branding=\"ChromeOS\" "
CHROMIUM_CORE_GN_DEFINES+=" enable_hevc_demuxing=true "
CHROMIUM_CORE_GN_DEFINES+=" enable_mse_mpeg2ts_stream_parser=true "
%ifarch %{ix86}
CHROMIUM_CORE_GN_DEFINES+=" target_cpu=\"x86\""
%endif
%ifarch %{x86_64}
CHROMIUM_CORE_GN_DEFINES+=" target_cpu=\"x64\""
%endif
%ifarch %{arm}
CHROMIUM_CORE_GN_DEFINES+=" target_cpu=\"arm\""
CHROMIUM_CORE_GN_DEFINES+=" remove_webcore_debug_symbols=true"
CHROMIUM_CORE_GN_DEFINES+=" rtc_build_with_neon=true"
%endif
%ifarch %{aarch64}
CHROMIUM_CORE_GN_DEFINES+=" target_cpu=\"arm64\""
%endif
CHROMIUM_CORE_GN_DEFINES+=" google_api_key=\"%{google_api_key}\""
CHROMIUM_CORE_GN_DEFINES+=" google_default_client_id=\"%{google_default_client_id}\""
CHROMIUM_CORE_GN_DEFINES+=" google_default_client_secret=\"%{google_default_client_secret}\""
CHROMIUM_CORE_GN_DEFINES+=" thin_lto_enable_optimizations=true use_clang=true use_lld=true use_thin_lto=true"
CHROMIUM_CORE_GN_DEFINES+=" custom_toolchain=\"//build/toolchain/linux/unbundle:default\""
CHROMIUM_CORE_GN_DEFINES+=" host_toolchain=\"//build/toolchain/linux/unbundle:default\""
CHROMIUM_CORE_GN_DEFINES+=" v8_snapshot_toolchain=\"//build/toolchain/linux/unbundle:default\""

CHROMIUM_BROWSER_GN_DEFINES="use_pulseaudio=true link_pulseaudio=true"
CHROMIUM_BROWSER_GN_DEFINES+=" enable_nacl=false"
CHROMIUM_BROWSER_GN_DEFINES+=" is_component_ffmpeg=true"
CHROMIUM_BROWSER_GN_DEFINES+=" enable_hangout_services_extension=true"
CHROMIUM_BROWSER_GN_DEFINES+=" use_aura=true"
CHROMIUM_BROWSER_GN_DEFINES+=" enable_widevine=true"
CHROMIUM_BROWSER_GN_DEFINES+=" enable_webrtc=true"
CHROMIUM_BROWSER_GN_DEFINES+=" use_vaapi=true"

if echo %{__cc} | grep -q clang; then
	export CFLAGS="%{optflags} -Qunused-arguments -fPIE -fpie -fPIC"
	export CXXFLAGS="%{optflags} -Qunused-arguments -fPIE -fpie -fPIC"
	_lto_cpus="$(getconf _NPROCESSORS_ONLN)"
	export LDFLAGS="%{ldflags} -Wl,--thinlto-jobs=$_lto_cpus"
	export AR="llvm-ar"
	export NM="llvm-nm"
	export RANLIB="llvm-ranlib"
else
	export CFLAGS="%{optflags}"
	export CXXFLAGS="%{optflags}"
fi
export CC=%{__cc}
export CXX=%{__cxx}

python2 tools/gn/bootstrap/bootstrap.py --skip-generate-buildfiles

python2 third_party/libaddressinput/chromium/tools/update-strings.py

out/Release/gn gen --script-executable=/usr/bin/python2 --args="${CHROMIUM_CORE_GN_DEFINES} ${CHROMIUM_BROWSER_GN_DEFINES}" out/Release

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
install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/%{name}/locales/
install -m 644 out/Release/chrome_100_percent.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/resources.pak %{buildroot}%{_libdir}/%{name}/
# May or may not be there depending on whether or not we use system icu
[ -e out/Release/icudtl.dat ] && install -m 644 out/Release/icudtl.dat %{buildroot}%{_libdir}/%{name}/
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
for i in 24 48 64 128 256; do
        mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
        install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
                %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install the master_preferences file
mkdir -p %{buildroot}%{_sysconfdir}/chromium
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/chromium

# FIXME ultimately Chromium should just use the system version
# instead of looking in its own directory... But for now, symlinking
# stuff where Chromium wants it will do
ln -s %{_libdir}/libGLESv2.so.2.1.0 %{buildroot}%{_libdir}/%{name}/libGLESv2.so
ln -s %{_libdir}/libEGL.so.1.1.0 %{buildroot}%{_libdir}/%{name}/libEGL.so
mkdir -p %{buildroot}%{_libdir}/%{name}/swiftshader
ln -s %{_libdir}/libGLESv2.so.2.1.0 %{buildroot}%{_libdir}/%{name}/swiftshader/libGLESv2.so
ln -s %{_libdir}/libEGL.so.1.1.0 %{buildroot}%{_libdir}/%{name}/swiftshader/libEGL.so

find %{buildroot} -name "*.nexe" -exec strip {} \;

# drirc workaround for VAAPI
mkdir -p %{buildroot}%{_datadir}/drirc.d/
cp %{S:4} %{buildroot}%{_datadir}/drirc.d/10-%{name}.conf

%if "%{channel}" == "stable"
%files -n chromium-browser
%endif

%files
%doc LICENSE AUTHORS
%config %{_sysconfdir}/chromium
%{_datadir}/drirc.d/10-%{name}.conf
%{_bindir}/%{name}
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/chromium-wrapper
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/chrome-sandbox
%optional %{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/chrome_100_percent.pak
%{_libdir}/%{name}/resources.pak
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/swiftshader
%{_libdir}/%{name}/themes
%{_libdir}/%{name}/default_apps
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files -n chromedriver%{namesuffix}
%doc LICENSE AUTHORS
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver
