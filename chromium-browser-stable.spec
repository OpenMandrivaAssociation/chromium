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
%bcond_with	system_icu
%bcond_without	system_ffmpeg
# Temporarily broken, cr_z_* symbols used even when we're supposed to use system minizip
%bcond_without	system_minizip
# chromium 58 fails with system vpx 1.6.1
%bcond_with	system_vpx
# system re2 doesn't work with custom libcxx
%bcond_with	system_re2

# Always support proprietary codecs
# or html5 does not work
%if %{with plf}
%define extrarelsuffix plf
%define distsuffix plf
%endif

Name: 		chromium-browser-%{channel}
# Working version numbers can be found at
# http://omahaproxy.appspot.com/
Version: 	85.0.4183.83
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
# Do not mangle libjpeg
Patch5:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-60.0.3112.78-jpeg-nomangle.patch
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
# rename function to avoid conflict with rawhide glibc "gettid()"
Patch50:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-75.0.3770.80-grpc-gettid-fix.patch
# Needs to be submitted..
Patch51:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-76.0.3809.100-gcc-remoting-constexpr.patch
# Needs to be submitted.. (ugly hack, needs to be added properly to GN files)
Patch52:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-78.0.3904.70-vtable-symbol-undefined.patch
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-unbundle-zlib.patch
Patch53:	chromium-81-unbundle-zlib.patch
# Needs to be submitted..
Patch54:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-77.0.3865.75-gcc-include-memory.patch
# https://chromium.googlesource.com/chromium/src/+/6b633c4b14850df376d5cec571699018772f358e
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-78-gcc-alignas.patch
Patch55:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-base-gcc-no-alignas.patch
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-78-protobuf-export.patch
Patch57:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-78-protobuf-export.patch
# https://gitweb.gentoo.org/repo/gentoo.git/plain/www-client/chromium/files/chromium-77-clang.patch
Patch59:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-77-clang.patch
# /../../ui/base/cursor/ozone/bitmap_cursor_factory_ozone.cc:53:15: error: 'find_if' is not a member of 'std'; did you mean 'find'? 
#Patch63:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-fix-find_if.patch


# Use lstdc++ on EPEL7 only
#Patch101:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-75.0.3770.100-epel7-stdc++.patch
# el7 only patch
#Patch102:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-el7-noexcept.patch

# Apply these patches to work around EPEL8 issues
#Patch300:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-76.0.3809.132-rhel8-force-disable-use_gnome_keyring.patch

Patch501:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-75.0.3770.80-SIOCGSTAMP.patch

### Chromium Tests Patches ###
# suse, system libs
Patch600:	arm_use_right_compiler.patch
# Arch Linux, fix for compile error with system ICU
Patch602:	https://raw.githubusercontent.com/archlinuxarm/PKGBUILDs/master/extra/chromium/chromium-system-icu.patch

# Enable VAAPI support on Linux
# Partially based on https://aur.archlinux.org/packages/chromium-vaapi/
Patch651:	vdpau-support.patch
Patch653:	chromium-skia-harmony.patch

# mga
Patch700:	chromium-81-extra-media.patch
Patch701:	chromium-69-wmvflvmpg.patch
Patch702:	chromium-40-sorenson-spark.patch

# omv
Patch1001:	chromium-64-system-curl.patch
Patch1002:	chromium-69-no-static-libstdc++.patch
Patch1003:	chromium-83-norar.patch
#Patch1004:	chromium-80-clang10-libstdc++10.patch
Patch1006:	chromium-81-dont-pretend-vaapi-is-broken.patch
Patch1007:	chromium-81-enable-gpu-features.patch

# stop so many build warnings
Patch1008:	chromium-71.0.3578.94-quieten.patch
Patch1009:	chromium-trace.patch

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
python2 build/linux/unbundle/remove_bundled_libraries.py \
	'base/third_party/cityhash' \
	'base/third_party/double_conversion' \
	'base/third_party/dynamic_annotations' \
	'base/third_party/icu' \
	'base/third_party/libevent' \
	'base/third_party/nspr' \
	'base/third_party/superfasthash' \
	'base/third_party/symbolize' \
	'base/third_party/valgrind' \
	'base/third_party/xdg_mime' \
	'base/third_party/xdg_user_dirs' \
	'buildtools/third_party/libc++' \
	'buildtools/third_party/libc++abi' \
	'chrome/third_party/mozilla_security_manager' \
	'courgette/third_party' \
	'net/third_party/mozilla_security_manager' \
	'net/third_party/nss' \
	'net/third_party/quic' \
	'net/third_party/uri_template' \
	'third_party/abseil-cpp' \
	'third_party/adobe' \
	'third_party/angle' \
	'third_party/angle/src/common/third_party/base' \
	'third_party/angle/src/common/third_party/smhasher' \
	'third_party/angle/src/common/third_party/xxhash' \
	'third_party/angle/src/third_party/compiler' \
	'third_party/angle/src/third_party/libXNVCtrl' \
	'third_party/angle/src/third_party/trace_event' \
	'third_party/angle/src/third_party/volk' \
	'third_party/angle/third_party/glslang' \
	'third_party/angle/third_party/spirv-headers' \
	'third_party/angle/third_party/spirv-tools' \
	'third_party/angle/third_party/vulkan-headers' \
	'third_party/angle/third_party/vulkan-loader' \
	'third_party/angle/third_party/vulkan-tools' \
	'third_party/angle/third_party/vulkan-validation-layers' \
	'third_party/apple_apsl' \
	'third_party/axe-core' \
	'third_party/blanketjs' \
	'third_party/blink' \
	'third_party/boringssl' \
	'third_party/boringssl/src/third_party/fiat' \
	'third_party/breakpad' \
	'third_party/breakpad/breakpad/src/third_party/curl' \
	'third_party/brotli' \
	'third_party/cacheinvalidation' \
	'third_party/catapult' \
	'third_party/catapult/common/py_vulcanize/third_party/rcssmin' \
	'third_party/catapult/common/py_vulcanize/third_party/rjsmin' \
	'third_party/catapult/third_party/beautifulsoup4' \
	'third_party/catapult/third_party/html5lib-python' \
	'third_party/catapult/third_party/polymer' \
	'third_party/catapult/third_party/six' \
	'third_party/catapult/tracing/third_party/d3' \
	'third_party/catapult/tracing/third_party/gl-matrix' \
	'third_party/catapult/tracing/third_party/jpeg-js' \
	'third_party/catapult/tracing/third_party/jszip' \
	'third_party/catapult/tracing/third_party/mannwhitneyu' \
	'third_party/catapult/tracing/third_party/oboe' \
	'third_party/catapult/tracing/third_party/pako' \
        'third_party/ced' \
	'third_party/cld_3' \
	'third_party/closure_compiler' \
	'third_party/crashpad' \
	'third_party/crashpad/crashpad/third_party/lss' \
	'third_party/crashpad/crashpad/third_party/zlib/' \
	'third_party/crc32c' \
	'third_party/cros_system_api' \
	'third_party/dav1d' \
	'third_party/dawn' \
	'third_party/depot_tools' \
	'third_party/devscripts' \
	'third_party/devtools-frontend' \
	'third_party/devtools-frontend/src/third_party/typescript' \
	'third_party/devtools-frontend/src/third_party/axe-core' \
	'third_party/devtools-frontend/src/front_end/third_party/acorn' \
	'third_party/devtools-frontend/src/front_end/third_party/codemirror' \
	'third_party/devtools-frontend/src/front_end/third_party/fabricjs' \
	'third_party/devtools-frontend/src/front_end/third_party/lighthouse' \
	'third_party/devtools-frontend/src/front_end/third_party/wasmparser' \
	'third_party/dom_distiller_js' \
	'third_party/emoji-segmenter' \
	'third_party/expat' \
	'third_party/ffmpeg' \
	'third_party/flac' \
        'third_party/flatbuffers' \
	'third_party/fontconfig' \
	'third_party/freetype' \
	'third_party/glslang' \
	'third_party/google_input_tools' \
	'third_party/google_input_tools/third_party/closure_library' \
	'third_party/google_input_tools/third_party/closure_library/third_party/closure' \
	'third_party/google_trust_services' \
	'third_party/googletest' \
	'third_party/grpc' \
	'third_party/grpc/src/third_party/nanopb' \
	'third_party/harfbuzz-ng' \
	'third_party/hunspell' \
	'third_party/iccjpeg' \
%if ! %{with system_icu}
	'third_party/icu' \
%endif
	'third_party/inspector_protocol' \
	'third_party/jinja2' \
	'third_party/jsoncpp' \
	'third_party/jstemplate' \
	'third_party/khronos' \
	'third_party/leveldatabase' \
	'third_party/libXNVCtrl' \
	'third_party/libaddressinput' \
	'third_party/libaom' \
	'third_party/libaom/source/libaom/third_party/vector' \
	'third_party/libaom/source/libaom/third_party/x86inc' \
	'third_party/libavif' \
	'third_party/libdrm' \
	'third_party/libgifcodec' \
	'third_party/libjingle' \
	'third_party/libjpeg_turbo' \
	'third_party/libphonenumber' \
	'third_party/libpng' \
	'third_party/libsecret' \
        'third_party/libsrtp' \
	'third_party/libsync' \
	'third_party/libudev' \
	'third_party/libusb' \
	'third_party/libvpx' \
	'third_party/libvpx/source/libvpx/third_party/x86inc' \
	'third_party/libwebm' \
	'third_party/libwebp' \
	'third_party/libxml' \
	'third_party/libxml/chromium' \
	'third_party/libxslt' \
	'third_party/libyuv' \
	'third_party/lottie' \
	'third_party/lss' \
	'third_party/lzma_sdk' \
	'third_party/mako' \
	'third_party/markupsafe' \
	'third_party/mesa' \
	'third_party/metrics_proto' \
%if %{with ozone}
	'third_party/minigbm' \
%endif
	'third_party/modp_b64' \
	'third_party/nasm' \
	'third_party/node' \
	'third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2' \
	'third_party/one_euro_filter' \
	'third_party/openh264' \
	'third_party/openscreen' \
	'third_party/openscreen/src/third_party/mozilla' \
	'third_party/openscreen/src/third_party/tinycbor' \
	'third_party/opencv' \
	'third_party/opus' \
	'third_party/ots' \
	'third_party/pdfium' \
	'third_party/pdfium/third_party/agg23' \
	'third_party/pdfium/third_party/base' \
	'third_party/pdfium/third_party/bigint' \
	'third_party/pdfium/third_party/freetype' \
	'third_party/pdfium/third_party/lcms' \
	'third_party/pdfium/third_party/libopenjpeg20' \
        'third_party/pdfium/third_party/libpng16' \
        'third_party/pdfium/third_party/libtiff' \
	'third_party/pdfium/third_party/skia_shared' \
	'third_party/perfetto' \
	'third_party/pffft' \
        'third_party/ply' \
	'third_party/polymer' \
	'third_party/private-join-and-compute' \
	'third_party/protobuf' \
	'third_party/protobuf/third_party/six' \
	'third_party/pyjson5' \
	'third_party/qcms' \
	'third_party/qunit' \
%if ! %{with system_re2}
	'third_party/re2' \
%endif
	'third_party/rnnoise' \
	'third_party/schema_org' \
	'third_party/s2cellid' \
	'third_party/simplejson' \
	'third_party/sinonjs' \
	'third_party/skia' \
	'third_party/skia/include/third_party/skcms' \
	'third_party/skia/include/third_party/vulkan' \
	'third_party/skia/third_party/skcms' \
	'third_party/skia/third_party/vulkan' \
	'third_party/smhasher' \
	'third_party/snappy' \
	'third_party/speech-dispatcher' \
	'third_party/spirv-headers' \
	'third_party/SPIRV-Tools' \
	'third_party/sqlite' \
	'third_party/swiftshader' \
	'third_party/swiftshader/third_party/astc-encoder' \
	'third_party/swiftshader/third_party/llvm-subzero' \
	'third_party/swiftshader/third_party/marl' \
	'third_party/swiftshader/third_party/subzero' \
	'third_party/swiftshader/third_party/SPIRV-Headers' \
	'third_party/tcmalloc' \
	'third_party/test_fonts' \
        'third_party/usb_ids' \
	'third_party/usrsctp' \
	'third_party/vulkan' \
%if %{with ozone}
	'third_party/wayland' \
%endif
	'third_party/web-animations-js' \
	'third_party/webdriver' \
	'third_party/webrtc' \
	'third_party/webrtc/common_audio/third_party/ooura' \
	'third_party/webrtc/common_audio/third_party/spl_sqrt_floor' \
	'third_party/webrtc/modules/third_party/fft' \
	'third_party/webrtc/modules/third_party/g711' \
	'third_party/webrtc/modules/third_party/g722' \
	'third_party/webrtc/rtc_base/third_party/base64' \
	'third_party/webrtc/rtc_base/third_party/sigslot' \
	'third_party/widevine' \
        'third_party/woff2' \
	'third_party/xcbproto' \
        'third_party/xdg-utils' \
        'third_party/zlib' \
	'third_party/zlib/google' \
	'tools/grit/third_party/six' \
	'url/third_party/mozilla' \
	'v8/src/third_party/siphash' \
	'v8/src/third_party/utf8-decoder' \
	'v8/src/third_party/valgrind' \
	'v8/third_party/v8' \
	'v8/third_party/inspector_protocol' \
	'tools/gn/src/base/third_party/icu' \
	--do-remove


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

export CC=clang
export CXX=clang++

# gn is rather convoluted and not python3 friendly -- let's make
# sure it sees python2 when it calls python
export PATH=`pwd`:$PATH

CHROMIUM_CORE_GN_DEFINES="use_sysroot=false is_debug=false fieldtrial_testing_like_official_build=true use_lld=false use_gold=true"
CHROMIUM_CORE_GN_DEFINES+=" is_clang=true clang_base_path=\"%{_prefix}\" clang_use_chrome_plugins=false "
CHROMIUM_CORE_GN_DEFINES+=" treat_warnings_as_errors=false use_custom_libcxx=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_libjpeg=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_lcms2=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_libpng=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_harfbuzz=true "
CHROMIUM_CORE_GN_DEFINES+=" use_system_libdrm=true "
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

gn_system_libraries="
    flac
    fontconfig
    freetype
    harfbuzz-ng
    libdrm
    libjpeg
    libusb
    libwebp
    libxslt
    snappy
"
#    libpng
#    opus
# cb - chrome 58
# libevent as system lib causes some hanging issues particularly with extensions
%if %{with system_re2}
gn_system_libraries+=" re2"
%endif

%if %{with system_minizip}
gn_system_libraries+=" zlib"
%endif
%if %{with system_icu}
gn_system_libraries+=" icu"
%endif
%if %{with system_vpx}
gn_system_libraries+=" libvpx"
%endif
%if %{with system_ffmpeg}
gn_system_libraries+=" ffmpeg"
%endif

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

python2 build/linux/unbundle/replace_gn_files.py --system-libraries ${gn_system_libraries}

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
mkdir -p %{buildroot}%{_libdir}/%{name}/swiftshader
ln -s %{_libdir}/libGLESv2.so.2.0.0 %{buildroot}%{_libdir}/%{name}/swiftshader/libGLESv2.so
ln -s %{_libdir}/libEGL.so.1.0.0 %{buildroot}%{_libdir}/%{name}/swiftshader/libEGL.so

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
%{_libdir}/%{name}/swiftshader

%files -n chromedriver%{namesuffix}
%doc LICENSE AUTHORS
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver
