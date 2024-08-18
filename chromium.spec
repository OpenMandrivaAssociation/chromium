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
# For incomplete debug package support
%define _empty_manifest_terminate_build 0

%ifarch %ix86
%define _build_pkgcheck_set %{nil}
%endif

%bcond_without browser
# Disabled for now because we need libc++ anyway (therefore
# can't use it in most other applications) and rust linkage
# fails in 126.x
%bcond_with cef
# Use the internal libc++ instead of libstdc++
# This should usually be avoided because of potential symbol
# clashes when using e.g. Qt and Chromium at the same time
# (especially with cef!), but some versions of chromium make
# it necessary
# in 124.x, chromium with libstdc++ crashes on startup.
%bcond_without libcxx

# FIXME As of 97.0.4688.2, Chromium crashes frequently when
# built with fortification enabled.
# [3784233:1:1107/202853.599120:ERROR:socket.cc(93)] sendmsg: Broken pipe (32)
# Received signal 11 <unknown> 03e900000001
#0 0x55af1960e344 (/usr/lib64/chromium-browser-dev/chrome+0x9071343)
#1 0x7fa28e947790 (/lib64/libc.so.6+0x4578f)
#2 0x7fa28e92e4f0 abort
#3 0x7fa28e98edc6 (/lib64/libc.so.6+0x8cdc5)
#4 0x7fa28ea386e2 __fortify_fail
#5 0x7fa28ea386b2 __stack_chk_fail
#6 0x55af1446e459 (/usr/lib64/chromium-browser-dev/chrome+0x3ed1458)
#7 0x7fa28e92fd8c (/lib64/libc.so.6+0x2dd8b)
#8 0x7fa28e92fe39 __libc_start_main
#9 0x55af140ab121 _start
# This should be investigated properly at some point.
%define _fortify_cflags %{nil}
%define _ssp_cflags %{nil}

# Libraries that should be unbundled (and reason why they
# aren't yet):
# openh264: Fails to compile
# icu: Causes crash when loading some websites, e.g.
#      build logs from abf, anti-spiegel.ru
# libevent: Seems to be ok in 125. Observed earlier:
#           Works-ish, but causes weird random freezes
#           observed e.g. while running multiple Slack
#           sessions in browser mode
# libvpx: Fails to compile
# re2 jsoncpp snappy: Use C++, therefore won't work while
#                     system uses libstdc++ but chromium
#                     uses use_custom_libcxx=true
# libaom (as of 118.x): Build error caused by GN insisting on in-tree version
# libwebp (as of 124.x): //third_party/libavif:libavif_enc(//build/toolchain/linux/unbundle:default) needs //third_party/libwebp:libwebp_sharpyuv(//build/toolchain/linux/unbundle:default)
# re2 (as of 124.x): //third_party/googletest:gtest_config(//build/toolchain/linux/unbundle:default) needs //third_party/re2:re2_config(//build/toolchain/linux/unbundle:default) (+ libc++/libstdc++ issue)
%if %{with libcxx}
%global system_libs brotli dav1d flac ffmpeg fontconfig harfbuzz-ng libjpeg libjxl libpng libdrm libxml libxslt opus libusb openh264 zlib freetype zstd libwebp libevent
%else
%global system_libs brotli dav1d flac ffmpeg fontconfig harfbuzz-ng libjpeg libjxl libpng libdrm libxml libxslt opus libusb openh264 zlib freetype zstd libwebp jsoncpp snappy libevent
%endif
%define system() %(if echo %{system_libs} |grep -q -E '(^| )%{1}( |$)'; then echo -n 1; else echo -n 0;  fi)

# Set up Google API keys, see http://www.chromium.org/developers/how-tos/api-keys
# OpenMandriva key, id and secret
# For your own builds, please get your own set of keys.
%define google_api_key AIzaSyAraWnKIFrlXznuwvd3gI-gqTozL-H-8MU
%define google_default_client_id 1089316189405-m0ropn3qa4p1phesfvi2urs7qps1d79o.apps.googleusercontent.com
%define google_default_client_secret RDdr-pHq2gStY4uw0m-zxXeo

%if "%{channel}" == "stable"
Name:		chromium
%else
Name:		chromium-browser-%{channel}
%endif
# Working version numbers can be found at
# https://chromiumdash.appspot.com/releases?platform=Linux
Version:	127.0.6533.119
### Don't be evil!!! ###
%define ungoogled 127.0.6533.119-1
%if %{with cef}
# To find the CEF commit matching the Chromium version, look up the
# right branch at
# https://bitbucket.org/chromiumembedded/cef/wiki/BranchesAndBuilding
# (Typically this will match the 3rd component of the version number)
# then check the commit for the branch at the branch download page,
# https://bitbucket.org/chromiumembedded/cef/downloads/?tab=branches
#
# Since we're using system libxml, we're potentially restoring
# https://github.com/chromiumembedded/cef/issues/3616 fixed in cef upstream.
# If we run into this problem, we need to either use custom libxml or build
# system libxml with TLS disabled.
%define cef 114ea2af1ba9da18c4ac5e599ccdbb17d01ba75a
%endif
Release:	1
Summary:	A fast webkit-based web browser
Group:		Networking/WWW
License:	BSD, LGPL
# From : http://gsdview.appspot.com/chromium-browser-official/
Source0:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
Source1:	chromium-wrapper
Source2:	chromium-browser%{namesuffix}.desktop
Source3:	master_preferences
# https://bugs.freedesktop.org/show_bug.cgi?id=106490
# Workaround from Arch Linux
# https://aur.archlinux.org/cgit/aur.git/tree/chromium-drirc-disable-10bpc-color-configs.conf?h=chromium-vaapi
Source4:	chromium-drirc-disable-10bpc-color-configs.conf
%if 0%{?cef:1}
Source10:	https://bitbucket.org/chromiumembedded/cef/get/%{cef}.tar.bz2
Source11:	https://chromium-fonts.storage.googleapis.com/336e775eec536b2d785cc80eff6ac39051931286#/test_fonts.tar.gz
%endif
Source100:	%{name}.rpmlintrc
%if 0%{?ungoogled:1}
Source1000:	https://github.com/ungoogled-software/ungoogled-chromium/archive/%{ungoogled}.tar.gz
%endif

# ============================================================================
# Patches 0 to 1999 are applied in the top level Chromium directory
# after ungoogled-chromium and cef patchsets have been applied.
# ============================================================================
# "Borrowed" from other distros (note we don't copy all their patches,
# just the ones that make sense for OM -- in particular no slew of
# workarounds for prehistoric libraries and compilers):
### 0-99: Fedora
# https://src.fedoraproject.org/rpms/chromium/tree/rawhide
%if ! 0%{?ungoogled:1}
# Ungoogled Chromium already builds a PIE sandbox
Patch0:		https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-70.0.3538.67-sandbox-pie.patch
%endif
# Use /etc/chromium for master_prefs
Patch1:		https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-68.0.3440.106-master-prefs-path.patch
Patch2:		https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-67.0.3396.62-gn-system.patch
Patch3:		https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-103.0.5060.53-update-rjsmin-to-1.2.0.patch
# Use gn system files
# Do not mangle zlib
Patch4:		https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-77.0.3865.75-no-zlib-mangle.patch
# Needs to be submitted..
Patch5:		https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-77.0.3865.75-gcc-include-memory.patch
Patch6:		https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-107-proprietary-codecs.patch
# Disable whitelist, allow everything
Patch7:		https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-122-disable-FFmpegAllowLists.patch

### 100-199: Arch
# https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=chromium-dev
# https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=chromium-wayland-vaapi
Patch100:	https://aur.archlinux.org/cgit/aur.git/plain/0001-ozone-wayland-implement-text_input_manager_v3.patch?h=chromium-wayland-vaapi#/0001-ozone-wayland-implement-text_input_manager_v3.patch
Patch101:	https://aur.archlinux.org/cgit/aur.git/plain/0001-ozone-wayland-implement-text_input_manager-fixes.patch?h=chromium-wayland-vaapi#/0001-ozone-wayland-implement-text_input_manager-fixes.patch
Patch102:	https://aur.archlinux.org/cgit/aur.git/plain/chromium-qt6.patch?h=chromium-dev#/chromium-qt6.patch
Patch103:	https://raw.githubusercontent.com/archlinux/svntogit-packages/packages/chromium/trunk/use-oauth2-client-switches-as-default.patch

### 200-299: Gentoo
Patch200:	https://gitweb.gentoo.org/repo/gentoo.git/plain/www-client/chromium/files/chromium-124-libwebp-shim-sharpyuv.patch

### 300-399: Debian
# https://sources.debian.org/patches/chromium/
# Mostly fixes for libstdc++ related failures
Patch300:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/ps-print.patch
Patch301:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/perfetto.patch
Patch302:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/blink-frags.patch
Patch303:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/material-utils.patch
Patch304:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/strlcpy.patch
Patch305:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/stats-collector.patch
Patch306:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/memory-allocator-dcheck-assert-fix.patch
Patch307:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/chromium-browser-ui-missing-deps.patch
Patch308:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/upstream/mojo.patch
Patch309:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/upstream/mojo-null.patch
Patch310:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/upstream/ruy-include.patch
Patch311:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/upstream/crabbyav1f.patch
Patch312:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/upstream/lock-impl.patch
Patch313:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/upstream/containers-header.patch
Patch314:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/upstream/paint-layer-header.patch
Patch315:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/disable/driver-chrome-path.patch
Patch316:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/disable/widevine-cdm-cu.patch
Patch317:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/disable/screen-ai-blob.patch
Patch318:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/system/icu-shim.patch
Patch319:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/system/jpeg.patch
Patch320:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/system/zlib.patch
Patch321:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/system/openjpeg.patch
Patch322:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/system/opus.patch
Patch323:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/system/eu-strip.patch
Patch324:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/system/rollup.patch
%if %{system libevent}
Patch337:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/system/event.patch
# Looks like Debian is missing a few spots... Let's add our own. Mixed in with the Debian
# patches because it's an addition to 334.
Patch338:	chromium-125-system-libevent.patch
%endif
Patch339:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/widevine-revision.patch
Patch340:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/widevine-locations.patch
Patch341:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/fixes/bindgen.patch
Patch342:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/disable/swiftshader.patch
Patch343:	https://sources.debian.org/data/main/c/chromium/127.0.6533.88-1/debian/patches/disable/swiftshader-2.patch

### 400-999: Patches from 3rd party projects that aren't distro packages
# https://gitlab.com/Matt.Jolly/chromium-patches
# Often has patches needed to build with libstdc++, sometimes other
# interesting bugs
Patch410:	https://raw.githubusercontent.com/ungoogled-software/ungoogled-chromium-fedora/master/chromium-91.0.4472.77-java-only-allowed-in-android-builds.patch
# From OBS CEF fork
# https://github.com/obsproject/cef/commits/6261-shared-textures
Patch420:	https://github.com/obsproject/cef/commit/27e977332df56c6251f4ee418d6bd51be073767d.patch
Patch421:	https://github.com/obsproject/cef/commit/f88220be4c4c02db5f9f0170dfc515d86a6f0c48.patch

### 1000+: Our own patches
Patch1001:	chromium-64-system-curl.patch
Patch1002:	chromium-69-no-static-libstdc++.patch
Patch1003:	chromium-system-zlib.patch
Patch1004:	chromium-107-system-libs.patch
# FIXME port
Patch1005:	chromium-restore-jpeg-xl-support.patch
Patch1006:	chromium-extra-widevine-search-paths.patch
Patch1007:	chromium-116-dont-override-thinlto-cache-policy.patch
Patch1008:	chromium-116-system-brotli.patch
#Patch1009:	chromium-97-compilefixes.patch
Patch1011:	perfetto-system-gn.patch
Patch1012:	chromium-105-minizip-ng.patch
#Patch1013:	chromium-126-compile.patch
Patch1014:	chromium-126-fix-build-on-non-ChromeOS-linux.patch
Patch1015:	chromium-113.0.5672.63-compile.patch
Patch1016:	chroimum-119-workaround-crash-on-startup.patch
# More and better search engines
# https://bugs.chromium.org/p/chromium/issues/detail?id=1502905
Patch1017:	chromium-124-search-engine-choice.patch
Patch1018:	chromium-81-unbundle-zlib.patch
Patch1019:	chromium-121-rust-clang_lib.patch
#Patch1020:	chromium-125-libstdc++.patch
Patch1021:	chromium-127-system-bindgen.patch
%if 0%{?cef:1}
Patch1022:	chromium-115-fix-generate_fontconfig_caches.patch
# FIXME probably needs porting
#Patch1023:	cef-115-minizip-ng.patch
%if 0%{?ungoogled:1}
# FIXME needs porting
Patch1024:	cef-126-rebase-to-ungoogled.patch
Patch1025:	cef-125-ungoogling.patch
%endif
Patch1026:	cef-zlib-linkage.patch
Patch1028:	cef-126-zlib-ng.patch
%endif
Patch1029:	chromium-127-minizip-ng.patch

# ============================================================================
# Patches 2000 to 2999 are applied inside the CEF tree.
# ============================================================================
# (we currently don't have any such patches)

# ============================================================================
# Patches 3000+ are from the various chromium upstream repositories
# and applied inside their respective directories.
# ============================================================================

# ============================================================================
# Patches 4000+ are applied inside the ungoogled-chromium tree before
# the ungoogling scripts are run
# ============================================================================

Provides:	%{crname}
Obsoletes:	chromium-browser-unstable < %{EVRD}
Obsoletes:	chromium-browser < %{EVRD}
%if "%{channel}" == "stable" || "%{channel}" == "beta"
Obsoletes:	chromium-browser-dev < %{EVRD}
%endif
%if "%{channel}" == "stable"
Obsoletes:	chromium-browser-beta < %{EVRD}
%rename chromium-browser-stable
%endif
BuildRequires:	glibc-static-devel
BuildRequires:	gperf
BuildRequires:	bison
BuildRequires:	re2c
BuildRequires:	flex
BuildRequires:	git
BuildRequires:	rust
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(krb5)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(com_err)
BuildRequires:	alsa-oss-devel
BuildRequires:	atomic-devel
BuildRequires:	snappy-devel
BuildRequires:	jsoncpp-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libva-drm)
BuildRequires:	pkgconfig(libva-glx)
BuildRequires:	pkgconfig(libva-x11)
BuildRequires:	pkgconfig(dri)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6OpenGL)
BuildRequires:	pkgconfig(RapidJSON)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(atspi-2)
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(atk-bridge-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libinput)
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	%{_lib}GL-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	clang lld
%if %{system brotli}
BuildRequires:	pkgconfig(libbrotlicommon)
BuildRequires:	pkgconfig(libbrotlidec)
BuildRequires:	pkgconfig(libbrotlienc)
BuildRequires:	brotli
%endif
%if %{system dav1d}
BuildRequires:	pkgconfig(dav1d)
%endif
%if %{system ffmpeg}
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavfilter)
BuildRequires:	pkgconfig(libavformat) >= 57.41.100
BuildRequires:	pkgconfig(libavutil)
%endif
%if %{system flac}
BuildRequires:	pkgconfig(flac)
%endif
%if %{system fontconfig}
BuildRequires:	pkgconfig(fontconfig)
%endif
%if %{system harfbuzz-ng}
BuildRequires:	harfbuzz-devel
%endif
%if %{system icu}
BuildRequires:	pkgconfig(icu-i18n)
%endif
%if %{system libaom}
BuildRequires:	pkgconfig(aom)
%endif
%if %{system libdrm}
BuildRequires:	pkgconfig(libdrm)
%endif
%if %{system libevent}
BuildRequires:	pkgconfig(libevent)
%endif
%if %{system libjpeg}
BuildRequires:	jpeg-devel
%endif
%if %{system libjxl}
BuildRequires:	pkgconfig(libjxl)
%endif
%if %{system libpng}
BuildRequires:	pkgconfig(libpng)
%endif
%if %{system libusb}
BuildRequires:	pkgconfig(libusb-1.0)
%endif
%if %{system libvpx}
BuildRequires:	pkgconfig(vpx)
%endif
%if %{system libwebp}
BuildRequires:	pkgconfig(libwebp)
%endif
%if %{system libxml}
BuildRequires:	pkgconfig(libxml-2.0)
%endif
%if %{system libxslt}
BuildRequires:	pkgconfig(libxslt)
%endif
%if %{system opus}
BuildRequires:	pkgconfig(opus)
%endif
%if %{system openh264}
BuildRequires:	pkgconfig(openh264)
%endif
%if %{system re2}
BuildRequires:	pkgconfig(re2)
%endif
%if %{system zlib}
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(minizip)
%endif
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xshmfence)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gl)
BuildRequires:	cups-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(xt)
BuildRequires:	cap-devel
BuildRequires:	elfutils-devel
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(snappy)

BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	python%{pyver}dist(protobuf)
BuildRequires:	python%{pyver}dist(markupsafe)

BuildRequires:	yasm
BuildRequires:	speech-dispatcher-devel
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	ninja
BuildRequires:	nodejs
BuildRequires:	jdk-current

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-browser-dev package instead.

%package qt5
Summary: Qt 5.x integration for Chromium
Group: System/Libraries
Requires: %{name} = %{EVRD}
Obsoletes: chromium-browser-stable-qt5

%description qt5
Qt 5.x integration for Chromium

%package qt6
Summary: Qt 6.x integration for Chromium
Group: System/Libraries
Requires: %{name} = %{EVRD}
Supplements: %{name} = %{EVRD}
Obsoletes: chromium-browser-stable-qt6

%description qt6
Qt 6.x integration for Chromium

%package -n cef-qt5
Summary: Qt 5.x integration for CEF
Group: System/Libraries
Requires: cef = %{EVRD}

%description -n cef-qt5
Qt 5.x integration for CEF

%package -n cef-qt6
Summary: Qt 6.x integration for CEF
Group: System/Libraries
Requires: cef = %{EVRD}
Supplements: cef = %{EVRD}

%description -n cef-qt6
Qt 6.x integration for CEF

%if 0%{?cef:1}
%package -n cef
Summary: Chromium Embedded Framework - library for embeddind Chromium in custom applications
# FIXME cef hardcodes a gtk dependency somewhere. It should
# really be dropped in favor of Qt
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(gtk+-unix-print-3.0)
Group: System/Libraries

%description -n cef
Chromium Embedded Framework - library for embeddind Chromium in custom applications

%package -n cef-devel
Summary: Chromium Embedded Framework - library for embeddind Chromium in custom applications
Group: Development/Libraries
Requires: cef = %{EVRD}

%description -n cef-devel
Chromium Embedded Framework - library for embeddind Chromium in custom applications
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
# Not using %%autosetup so we can apply patches after
# ungoogled-chromium patches have been applied
%setup -q -n chromium-%{version} %{?ungoogled:-a 1000}

%if 0%{?ungoogled:1}
UGDIR=$(pwd)/ungoogled-chromium-%{ungoogled}
# Add a Source1001 patch whenever UG is behind upstream
cd $UGDIR
%autopatch -p1 -m 4000
cd ..
echo %{version} >$UGDIR/chromium_version.txt
# Disable a few patches: We don't want to allow Google to spy on our
# users, but we don't want to prevent users from voluntarily using
# Google services.
# Also, disable some security-for-usability tradeoffs by default
sed -i \
	-e '/disable-autofill/d' \
	-e '/prefs-only-keep-cookies-until-exit/d' \
	$UGDIR/patches/series
python $UGDIR/utils/prune_binaries.py ./ $UGDIR/pruning.list --verbose
python $UGDIR/utils/patches.py apply ./ $UGDIR/patches
python $UGDIR/utils/domain_substitution.py apply -r $UGDIR/domain_regex.list -f $UGDIR/domain_substitution.list -c domainsubcache.tar.gz ./
%endif

%if 0%{?cef:1}
tar xf %{S:10}
mv chromiumembedded-cef-* cef
# CEF's scripts refuse to work outside of git repositories, so
# we have to fake it
git init
cd third_party/pdfium ; git init; cd ../..
cd cef; git init; cd ..
cd cef
%autopatch -p1 -m 2000 -M 2999
COMMIT_NUMBER=%(echo %{version} |cut -d. -f3) COMMIT_HASH=%{cef} python tools/make_version_header.py include/cef_version.h --cef_version VERSION.in --chrome_version ../chrome/VERSION --cpp_header_dir include
cd ..

cd third_party/test_fonts
tar xf %{S:11}
cd ../..
%endif

%autopatch -p1 -M 1999

cd third_party/webrtc
%autopatch -p1 -m 3000 -M 3009
cd -
cd media
%autopatch -p1 -m 3010 -M 3019
cd -

rm -rf third_party/binutils/
# Get rid of the pre-built eu-strip binary, it is x86_64 and of mysterious origin
rm -rf buildtools/third_party/eu-strip/bin/eu-strip
  
# Replace it with a symlink to the system copy
ln -s %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

echo "%{revision}" > build/LASTCHANGE.in

#sed -i 's!-nostdlib++!!g'  build/config/posix/BUILD.gn
sed -i 's!ffmpeg_buildflags!ffmpeg_features!g' build/linux/unbundle/ffmpeg.gn

# Allow building against system libraries in official builds
sed -i 's/OFFICIAL_BUILD/GOOGLE_CHROME_BUILD/' \
	tools/generate_shim_headers/generate_shim_headers.py

# Hard code extra version
FILE=chrome/common/channel_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"%{product_vendor} %{product_version}"/' $FILE
cmp $FILE $FILE.orig && exit 1

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
python build/linux/unbundle/replace_gn_files.py \
	--system-libraries %{system_libs}
# Forcing an outdated copy of what should really match system headers
# is just about as dumb as something can get
cp -f %{_includedir}/wayland-client-core.h third_party/wayland/src/src/

# workaround build failure
if [ ! -f chrome/test/data/webui/i18n_process_css_test.html ]; then
	touch chrome/test/data/webui/i18n_process_css_test.html
fi

%build
%if 0%{?ungoogled:1}
UGDIR=$(pwd)/ungoogled-chromium-%{ungoogled}
%endif

. %{_sysconfdir}/profile.d/90java.sh

%ifarch %{arm}
# Use linker flags to reduce memory consumption on low-mem architectures
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
%global optflags %(echo %{optflags} | sed -e 's/-g3 /-g1 /')
%global optflags %{optflags} -I%{_includedir}/libunwind

# Chromium builds tend to barf if not told precisely what to use
export CC="%{__cc}"
export CXX="%{__cxx}"
export AR="%{__ar}"
export NM="llvm-nm"

_lto_cpus="$(getconf _NPROCESSORS_ONLN)"
if [ $_lto_cpus -gt 4 ]; then
	# LTO is very memory intensive, so
	# 32 parallel LTO jobs may not be
	# a good idea...
	_lto_cpus=4
fi

# FIXME error: the option `Z` is only accepted on the nightly compiler
export RUSTC_BOOTSTRAP=1

%if "%{_lib}" != "lib"
# Something hardcodes ../../[...]/usr/lib as LIBCLANG_PATH
# which of course doesn't catch lib64 and friends...
sed -i -e "s,args.libclang_path,'%{_libdir}',g" build/rust/run_bindgen.py
sed -i -e 's,lib/clang,%{_lib}/clang,g' build/rust/rust_bindgen.gni
%endif

GN_DEFINES=""
%if 0%{?ungoogled:1}
GN_DEFINES+=" $(cat $UGDIR/flags.gn |tr '\n' ' ')"
%endif
GN_DEFINES+="use_sysroot=false is_debug=false "
GN_DEFINES+=" is_clang=true clang_base_path=\"%{_prefix}\" clang_use_chrome_plugins=false "
GN_DEFINES+=" treat_warnings_as_errors=false "
%if %{with libcxx}
GN_DEFINES+=" use_custom_libcxx=true "
%else
GN_DEFINES+=" use_custom_libcxx=false "
%endif
for i in %{system_libs}; do
	if [ "$i" = "harfbuzz-ng" ]; then
		GN_DEFINES+=" use_system_harfbuzz=true "
	else
		GN_DEFINES+=" use_system_$i=true "
	fi
done
GN_DEFINES+=" use_system_expat=true "
GN_DEFINES+=" use_system_lcms2=true "
GN_DEFINES+=" use_system_libffi=true "
GN_DEFINES+=" use_system_libopenjpeg2=true "
# We don't currently ship libsync
#GN_DEFINES+=" use_system_libsync=true "
GN_DEFINES+=" use_system_libwayland=true "
GN_DEFINES+=" use_system_libwayland_client=true "
GN_DEFINES+=" use_system_libwayland_server=true "
GN_DEFINES+=" use_system_lua=true "
GN_DEFINES+=" use_system_minigbm=true "
GN_DEFINES+=" use_system_openjpeg2=true "
GN_DEFINES+=" use_system_protobuf=true "
GN_DEFINES+=" use_system_wayland=true "
GN_DEFINES+=" use_system_wayland_client=true "
GN_DEFINES+=" use_system_wayland_scanner=true "
GN_DEFINES+=" use_system_wayland_server=true "
GN_DEFINES+=" use_xkbcommon=true "
GN_DEFINES+=" use_gtk=true gtk_version=4 use_qt=true use_qt6=true moc_qt6_path=\"%{_qtdir}/libexec\""
if ! echo %{system_libs} |grep -q icu; then
GN_DEFINES+=" icu_use_data_file=true"
fi
GN_DEFINES+=" use_gnome_keyring=false "
GN_DEFINES+=" fatal_linker_warnings=false "
GN_DEFINES+=" system_libdir=\"%{_libdir}\""
#GN_DEFINES+=" use_aura=true "
#GN_DEFINES+=" use_gio=true"
GN_DEFINES+=" enable_nacl=false "
GN_DEFINES+=" proprietary_codecs=true "
GN_DEFINES+=" ffmpeg_branding=\"ChromeOS\" "
GN_DEFINES+=" enable_mse_mpeg2ts_stream_parser=true "
%ifarch %{ix86}
GN_DEFINES+=" target_cpu=\"x86\""
%endif
%ifarch %{x86_64}
GN_DEFINES+=" target_cpu=\"x64\""
%endif
%ifarch %{arm}
GN_DEFINES+=" target_cpu=\"arm\""
GN_DEFINES+=" remove_webcore_debug_symbols=true"
%endif
%ifarch %{armx}
GN_DEFINES+=" rtc_build_with_neon=true"
%endif
%ifarch %{aarch64}
GN_DEFINES+=" target_cpu=\"arm64\""
# if this is true (default for non official builds) it tries to use
# a prebuilt x86 binary in the source tree
GN_DEFINES+=" devtools_skip_typecheck=false"
%endif
%if ! 0%{?ungoogled:1}
GN_DEFINES+=" google_api_key=\"%{google_api_key}\""
GN_DEFINES+=" google_default_client_id=\"%{google_default_client_id}\""
GN_DEFINES+=" google_default_client_secret=\"%{google_default_client_secret}\""
%endif
GN_DEFINES+=" thin_lto_enable_optimizations=true use_lld=true use_thin_lto=true"
GN_DEFINES+=" custom_toolchain=\"//build/toolchain/linux/unbundle:default\""
GN_DEFINES+=" host_toolchain=\"//build/toolchain/linux/unbundle:default\""
GN_DEFINES+=" v8_snapshot_toolchain=\"//build/toolchain/linux/unbundle:default\""
GN_DEFINES+=" symbol_level=1"

GN_DEFINES+=" use_pulseaudio=true link_pulseaudio=true"
GN_DEFINES+=" enable_nacl=false"
GN_DEFINES+=" is_component_ffmpeg=true"
GN_DEFINES+=" enable_hangout_services_extension=true"
GN_DEFINES+=" enable_widevine=true"
GN_DEFINES+=" use_vaapi=true"
GN_DEFINES+=" angle_link_glx=true angle_test_enable_system_egl=true "
GN_DEFINES+=" enable_hevc_parser_and_hw_decoder=true enable_av1_decoder=true enable_jxl_decoder=true"
GN_DEFINES+=" enable_media_drm_storage=true"
%ifarch znver1
# This really is znver1 only, as it enables SSE4.2, BMI2 and AVX2
GN_DEFINES+=" enable_perfetto_x64_cpu_opt=true"
%endif
GN_DEFINES+=" enable_precompiled_headers=true"
GN_DEFINES+=" is_official_build=true"
GN_DEFINES+=" ozone_platform_drm=true"
GN_DEFINES+=" perfetto_use_system_zlib=true"
GN_DEFINES+=" rtc_link_pipewire=true rtc_use_pipewire=true"
GN_DEFINES+=" use_libinput=true use_real_dbus_clients=true"
GN_DEFINES+=" use_vaapi_image_codecs=true"
GN_DEFINES+=' rust_sysroot_absolute="%{_prefix}"'
GN_DEFINES+=" rustc_version=\"$(rustc --version | awk '{ print $2; }')\""
# 107: Build failure: GN_DEFINES+=" enable_wayland_server=true"
# 124: Fails with 
# ld.lld: error: undefined symbol: google::protobuf::compiler::CodeGenerator::GenerateAll(std::__Cr::vector<google::protobuf::FileDescriptor const*, std::__Cr::allocator<google::protobuf::FileDescriptor const*>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, google::protobuf::compiler::GeneratorContext*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>*) const
# >>> referenced by ld-temp.o
# (probably hardcoded use of bundled headers somewhere...)
#GN_DEFINES+=" perfetto_use_system_protobuf=true"
GN_DEFINES+=" use_v4lplugin=true"
# Can't use vaapi and v4l2_codec at the same time, there is no
# selection at runtime
# GN_DEFINES+=" use_v4l2_codec=true"
GN_DEFINES+=" use_webaudio_ffmpeg=true"

# -gdwarf-4 is for the sake of debugedit
# https://sourceware.org/bugzilla/show_bug.cgi?id=29773
if echo %{__cc} | grep -q clang; then
	export CFLAGS="%{optflags} -Qunused-arguments -fPIE -fpie -fPIC -gdwarf-4"
	export CXXFLAGS="%{optflags} -Qunused-arguments -fPIE -fpie -fPIC -gdwarf-4"
	if echo %{optflags} |grep -qE -- '-O[sz]'; then
		# FIXME this should get a real fix
		# _Float32 acts up with -Os/-Oz [at compile time]
		export CFLAGS="$CFLAGS -O2"
		export CXXFLAGS="$CXXFLAGS -O2"
	fi
	export LDFLAGS="%{build_ldflags} -Wl,--thinlto-jobs=$_lto_cpus"
	export AR="llvm-ar"
	export NM="llvm-nm"
	export RANLIB="llvm-ranlib"
else
	export CFLAGS="%{optflags}"
	export CXXFLAGS="%{optflags}"
fi
export CC="%{__cc}"
export CXX="%{__cxx}"

python tools/gn/bootstrap/bootstrap.py --skip-generate-buildfiles

python third_party/libaddressinput/chromium/tools/update-strings.py

%if %{with browser}
out/Release/gn gen --script-executable=/usr/bin/python --args="${GN_DEFINES}" out/Release

%ifarch %{x86_64}
ninja -C out/Release chrome chrome_sandbox chromedriver
%else
ninja -C out/Release chrome chrome_sandbox
%endif
%endif

%if 0%{?cef:1}
# Apply CEF specific patches and build CEF...
cd cef
./tools/patch.sh
cd ..

# Lastly, try to build it...
# We have to use use_thin_lto=false because LTO in CEF causes
# an OOM while linking libcef.so even on boxes with 64 GB RAM + 64 GB swap
out/Release/gn gen --script-executable=/usr/bin/python --args="${GN_DEFINES} is_cfi=false use_thin_lto=false chrome_pgo_phase=0" out/Release-CEF
ninja -C out/Release-CEF cef chrome_sandbox
%endif

%install
%if %{with browser}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}/locales
mkdir -p %{buildroot}%{_libdir}/%{name}/themes
mkdir -p %{buildroot}%{_libdir}/%{name}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{SOURCE1} %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/chrome %{buildroot}%{_libdir}/%{name}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_libdir}/%{name}/chrome-sandbox
install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/%{name}/locales/
install -m 644 out/Release/chrome_100_percent.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/libqt5_shim.so %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/libqt6_shim.so %{buildroot}%{_libdir}/%{name}/
# libGLESv2.so/libEGL.so look like dupes from the system, but aren't:
# Loading happens in ui/ozone/common/egl_util.cc -- indicating libGLESv2.so
# and libEGL.so (as opposed to their .1/.2 counterparts) are ANGLE (OpenGL ES
# -> native GL API wrapper)
# Now for most HW that shouldn't be necessary, so we may want to get rid of
# the custom libs and just use Mesa's libraries directly at some point.
install -m 755 out/Release/libGLESv2.so %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/libEGL.so %{buildroot}%{_libdir}/%{name}/
# ANGLE data files (fake ICD for custom vulkan bits?), probably needed unless and
# until we drop the custom libEGL/libGLESv2
cp -a out/Release/angledata %{buildroot}%{_libdir}/%{name}/
cp out/Release/vk_swiftshader_icd.json %{buildroot}%{_libdir}/%{name}/
# FIXME is the custom vulkan needed, or is this just dupes from system vulkan
# for prehistoric distros?
install -m 755 out/Release/libvulkan.so.1 %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/libvk_swiftshader.so %{buildroot}%{_libdir}/%{name}/
# May or may not be there depending on whether or not we use system icu
[ -e out/Release/icudtl.dat ] && install -m 644 out/Release/icudtl.dat %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/*.bin %{buildroot}%{_libdir}/%{name}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_libdir}/%{name}/default_apps/
ln -s %{_libdir}/%{name}/chromium-wrapper %{buildroot}%{_bindir}/%{name}
%ifarch %{x86_64}
cp -a out/Release/chromedriver %{buildroot}%{_libdir}/%{name}/chromedriver
ln -s %{_libdir}/%{name}/chromedriver %{buildroot}%{_bindir}/chromedriver
%endif

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

find %{buildroot} -name "*.nexe" -exec strip {} \;

# drirc workaround for VAAPI
mkdir -p %{buildroot}%{_datadir}/drirc.d/
cp %{S:4} %{buildroot}%{_datadir}/drirc.d/10-%{name}.conf
%endif

%if 0%{?cef:1}
# FIXME the packaging here is based on the filesystem layout in
# the binaries referenced in OnlyOffice's
# https://github.com/ONLYOFFICE/build_tools/blob/master/scripts/core_common/modules/cef.py
# such as
# http://d2ettrnqo7v976.cloudfront.net/cef/5414/linux_64/cef_binary.7z
# Is there a better option?
# Adding qt5_shim/qt6_shim stuff is OM specific, hoping to get Qt integration
cd out/Release-CEF
mkdir -p %{buildroot}%{_libdir}/cef/Release \
	%{buildroot}%{_libdir}/cef/Resources
cp -a chrome_sandbox libcef.so libEGL.so libGLESv2.so libvk_swiftshader.so libvulkan.so.1 snapshot_blob.bin v8_context_snapshot.bin vk_swiftshader_icd.json libqt5_shim.so libqt6_shim.so %{buildroot}%{_libdir}/cef/Release
# The build process generates chrome_sandbox, but cef binary builds ship chrome-sandbox
# It's the same thing, so let's provide both names to be on the safe side
ln -s chrome_sandbox %{buildroot}%{_libdir}/cef/Release/chrome-sandbox
cp -a chrome_100_percent.pak chrome_200_percent.pak icudtl.dat locales resources.pak %{buildroot}%{_libdir}/cef/Resources
# This is expected by the OBS browser plugin
mkdir -p %{buildroot}%{_libdir}/cef/libcef_dll_wrapper
cd obj/cef
# libcef_dll_wrapper.a is a thin archive, containing references to the object
# files rather than the object files themselves
llvm-ar -t libcef_dll_wrapper.a |xargs llvm-ar cru libcef_dll_wrapper_full.a
mv -f libcef_dll_wrapper_full.a libcef_dll_wrapper.a
llvm-ranlib libcef_dll_wrapper.a
cp libcef_dll_wrapper.a %{buildroot}%{_libdir}/cef/libcef_dll_wrapper
cd ../../../..

# -devel package layout is based on what we see in OnlyOffice's
# desktop-sdk/ChromiumBasedEditors/lib/src/cef/linux
cp -a cef/include %{buildroot}%{_libdir}/cef/
cp -a out/Release-CEF/includes/cef/include/* %{buildroot}%{_libdir}/cef/include/
# Header referenced by cef but not included there
mkdir -p %{buildroot}%{_libdir}/cef/include/base/internal/net/base
cp -a net/base/net_error_list.h %{buildroot}%{_libdir}/cef/include/base/internal/net/base/
cp -a cef/libcef_dll cef/tests %{buildroot}%{_libdir}/cef

%files -n cef
%dir %{_libdir}/cef
%{_libdir}/cef/Release
%exclude %{_libdir}/cef/Release/libqt5_shim.so
%exclude %{_libdir}/cef/Release/libqt6_shim.so
%{_libdir}/cef/Resources

%files -n cef-qt5
%{_libdir}/cef/Release/libqt5_shim.so

%files -n cef-qt6
%{_libdir}/cef/Release/libqt6_shim.so

%files -n cef-devel
%{_libdir}/cef/include
%{_libdir}/cef/libcef_dll
%{_libdir}/cef/tests
%{_libdir}/cef/libcef_dll_wrapper
%endif

%if %{with browser}
%files
%doc LICENSE AUTHORS
%config %{_sysconfdir}/chromium
%{_datadir}/drirc.d/10-%{name}.conf
%{_bindir}/%{name}
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.so*
%exclude %{_libdir}/%{name}/libqt5_shim.so
%exclude %{_libdir}/%{name}/libqt6_shim.so
%{_libdir}/%{name}/*.json
%{_libdir}/%{name}/angledata
%{_libdir}/%{name}/chromium-wrapper
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/chrome-sandbox
%optional %{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/chrome_100_percent.pak
%{_libdir}/%{name}/resources.pak
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/themes
%{_libdir}/%{name}/default_apps
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files qt5
%{_libdir}/%{name}/libqt5_shim.so

%files qt6
%{_libdir}/%{name}/libqt6_shim.so

%ifarch %{x86_64}
%files -n chromedriver%{namesuffix}
%doc LICENSE AUTHORS
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver
%endif
%endif

%clean
# don't wipe BUILD
