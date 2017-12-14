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
# Chromium breaks on wayland, hidpi, and colors with gtk3 enabled.
# But as of 60.0.3112.78 and .90, building with gtk2 is broken
%bcond_without	gtk3
# crisb - ozone causes a segfault on startup as of 57.0.2987.133
%bcond_with	ozone
%bcond_with	system_icu
%bcond_without	system_ffmpeg
# Temporarily broken, cr_z_* symbols used even when we're supposed to use system minizip
%bcond_with	system_minizip
# chromium 58 fails with system vpx 1.6.1
%bcond_with	system_vpx
%bcond_with	system_harfbuzz

# Always support proprietary codecs
# or html5 does not work
%if %{with plf}
%define extrarelsuffix plf
%define distsuffix plf
%endif

Name: 		chromium-browser-stable
# Working version numbers can be found at
# http://omahaproxy.appspot.com/
Version: 	63.0.3239.108
Release: 	1%{?extrarelsuffix}
Summary: 	A fast webkit-based web browser
Group: 		Networking/WWW
License: 	BSD, LGPL
# From : http://gsdview.appspot.com/chromium-browser-official/
Source0: 	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
Source1: 	chromium-wrapper
Source2: 	chromium-browser.desktop
Source3:	master_preferences

%if %mdvver >= 201500
# Don't use clang's integrated as while trying to check the version of gas
#Patch4:		chromium-36.0.1985.143-clang-no-integrated-as.patch
%endif

#Patch20:	chromium-last-commit-position-r0.patch

### Chromium Fedora Patches ###
Patch0:         chromium-56.0.2924.87-gcc5.patch
Patch1:         chromium-45.0.2454.101-linux-path-max.patch
Patch2:         chromium-55.0.2883.75-addrfix.patch
Patch4:         chromium-46.0.2490.71-notest.patch
# Ignore broken nacl open fd counter
Patch7:         chromium-47.0.2526.80-nacl-ignore-broken-fd-counter.patch
Patch8:		chromium-63-system-clang.patch
# Use libusb_interrupt_event_handler from current libusbx (1.0.21-0.1.git448584a)
Patch9:         chromium-48.0.2564.116-libusb_interrupt_event_handler.patch
Patch10:	chromium-64-system-curl.patch
# Ignore deprecations in cups 2.2
# https://bugs.chromium.org/p/chromium/issues/detail?id=622493
Patch12:        chromium-55.0.2883.75-cups22.patch
# Use PIE in the Linux sandbox (from openSUSE via Russian Fedora)
Patch15:        chromium-55.0.2883.75-sandbox-pie.patch
# Enable ARM CPU detection for webrtc (from archlinux via Russian Fedora)
Patch16:        chromium-52.0.2743.82-arm-webrtc.patch
# Use /etc/chromium for master_prefs
Patch18:        chromium-52.0.2743.82-master-prefs-path.patch
# Use gn system files
Patch20:        chromium-54.0.2840.59-gn-system.patch
# Fix last commit position issue
# https://groups.google.com/a/chromium.org/forum/#!topic/gn-dev/7nlJv486bD4
Patch21:        chromium-53.0.2785.92-last-commit-position.patch
# Fix issue where timespec is not defined when sys/stat.h is included.
Patch22:        chromium-53.0.2785.92-boringssl-time-fix.patch
# I wouldn't have to do this if there was a standard way to append extra compiler flags
Patch24:        http://pkgs.fedoraproject.org/cgit/rpms/chromium.git/plain/chromium-59.0.3071.86-nullfix.patch
# Add explicit includedir for jpeglib.h
Patch25:        chromium-54.0.2840.59-jpeg-include-dir.patch
# On i686, pass --no-keep-memory --reduce-memory-overheads to ld.
Patch26:        http://pkgs.fedoraproject.org/cgit/rpms/chromium.git/plain/chromium-59.0.3071.86-i686-ld-memory-tricks.patch
# obj/content/renderer/renderer/child_frame_compositing_helper.o: In function `content::ChildFrameCompositingHelper::OnSetSurface(cc::SurfaceId const&, gfx::Size const&, float, cc::SurfaceSequence const&)':
# /builddir/build/BUILD/chromium-54.0.2840.90/out/Release/../../content/renderer/child_frame_compositing_helper.cc:214: undefined reference to `cc_blink::WebLayerImpl::setOpaque(bool)'
#Patch27:        http://pkgs.fedoraproject.org/cgit/rpms/chromium.git/plain/chromium-59.0.3071.86-setopaque.patch
# Use -fpermissive to build WebKit
Patch31:        chromium-56.0.2924.87-fpermissive.patch

# suse, system libs
Patch103:	arm_use_right_compiler.patch
#Patch104:	https://gitweb.gentoo.org/repo/gentoo.git/plain/www-client/chromium/files/chromium-system-ffmpeg-r6.patch
Patch105:	chromium-system-jinja-r13.patch

# mga
Patch111:	chromium-55-extra-media.patch
Patch112:	chromium-40-wmvflvmpg.patch
Patch114:	chromium-55-flac.patch

# omv
Patch120:	chromium-59-clang-workaround.patch
Patch123:	chromium-61.0.3163.100-glibc-2.26.patch

Provides: 	%{crname}
Obsoletes: 	chromium-browser-unstable < 26.0.1410.51
Obsoletes: 	chromium-browser-beta < 26.0.1410.51
Obsoletes: 	chromium-browser < 1:9.0.597.94
BuildRequires: 	gperf
BuildRequires: 	bison
BuildRequires: 	re2c
BuildRequires: 	flex
#BuildRequires: 	v8-devel
BuildRequires: 	alsa-oss-devel
%if %mdvver >= 201500
BuildRequires:	atomic-devel
BuildRequires:	harfbuzz-devel
%else
BuildRequires:	%{_lib}atomic1
%endif
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires: 	snappy-devel
BuildRequires: 	jsoncpp-devel
BuildRequires: 	pkgconfig(expat)
BuildRequires: 	pkgconfig(glib-2.0)
# FIXME we currently can't use system re2 because
# Chromium uses libc++ while the system STL is libstdc++ for now
# This leads to unresolved symbols because of disagreements over
# the namespace of std::basic_string (__1 vs. not __1)
#BuildRequires:	pkgconfig(re2)
BuildRequires: 	pkgconfig(wayland-egl)
BuildRequires: 	pkgconfig(nss)
BuildRequires: 	bzip2-devel
BuildRequires: 	jpeg-devel
BuildRequires: 	pkgconfig(libpng)
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
%if %{with system_minizip}
BuildRequires: 	pkgconfig(minizip)
%endif
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
BuildRequires:	nodejs
BuildRequires:	python2-markupsafe
BuildRequires:	python2-ply
BuildRequires:	python2-beautifulsoup4
BuildRequires:	python2-simplejson
BuildRequires:	python2-html5lib

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
Summary:	WebDriver for Google Chrome/Chromium
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}


%description -n chromedriver
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.


%prep
%setup -q -n chromium-%{version}
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

# use the system nodejs
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s /usr/bin/node third_party/node/linux/node-linux-x64/bin/

# Remove bundled libs
python2 build/linux/unbundle/remove_bundled_libraries.py \
	'third_party/ffmpeg' \
	'third_party/adobe' \
	'third_party/blink' \
	'third_party/blink/tools' \
	'third_party/blink/tools/blinkpy' \
	'third_party/blink/tools/blinkpy/common' \
	'third_party/breakpad' \
	'third_party/flac' \
	'third_party/glslang-angle' \
	'third_party/harfbuzz-ng' \
	'third_party/icu' \
	'base/third_party/libevent' \
	'third_party/libdrm' \
	'third_party/libjpeg_turbo' \
	'third_party/libpng' \
	'third_party/libsrtp' \
	'third_party/libwebp' \
	'third_party/libxml' \
	'third_party/libxslt' \
	'third_party/openh264' \
	'third_party/re2' \
	'third_party/snappy' \
	'third_party/speech-dispatcher' \
	'third_party/spirv-tools-angle' \
	'third_party/spirv-headers' \
	'third_party/swiftshader' \
	'third_party/swiftshader/third_party/subzero' \
	'third_party/swiftshader/third_party/LLVM' \
	'third_party/swiftshader/third_party/llvm-subzero' \
	'third_party/usb_ids' \
	'third_party/vulkan-validation-layers' \
	'third_party/xdg-utils' \
	'third_party/yasm' \
	'third_party/zlib' \
	'base/third_party/dmg_fp' \
	'base/third_party/dynamic_annotations' \
	'base/third_party/icu' \
	'base/third_party/nspr' \
	'base/third_party/superfasthash' \
	'base/third_party/symbolize' \
	'base/third_party/valgrind' \
	'base/third_party/xdg_mime' \
	'base/third_party/xdg_user_dirs' \
	'chrome/third_party/mozilla_security_manager' \
	'courgette/third_party' \
	'native_client_sdk/src/libraries/third_party/newlib-extras' \
	'native_client/src/third_party/dlmalloc' \
	'native_client/src/third_party/valgrind' \
	'net/third_party/mozilla_security_manager' \
	'net/third_party/nss' \
	'third_party/WebKit' \
	'third_party/analytics' \
	'third_party/angle' \
	'third_party/angle/src/common/third_party/base' \
	'third_party/angle/src/common/third_party/smhasher' \
	'third_party/angle/src/third_party/compiler' \
	'third_party/angle/src/third_party/libXNVCtrl' \
	'third_party/angle/src/third_party/trace_event' \
	'third_party/blanketjs' \
	'third_party/boringssl' \
	'third_party/brotli' \
	'third_party/cacheinvalidation' \
	'third_party/catapult' \
	'third_party/catapult/tracing/third_party/d3' \
	'third_party/catapult/tracing/third_party/gl-matrix' \
	'third_party/catapult/tracing/third_party/jszip' \
	'third_party/catapult/tracing/third_party/mannwhitneyu' \
	'third_party/catapult/tracing/third_party/oboe' \
	'third_party/catapult/tracing/third_party/pako' \
	'third_party/catapult/third_party/polymer' \
	'third_party/catapult/common/py_vulcanize' \
	'third_party/catapult/common/py_vulcanize/third_party/rcssmin' \
	'third_party/catapult/common/py_vulcanize/third_party/rjsmin' \
	'third_party/ced' \
	'third_party/cld_2' \
	'third_party/cld_3' \
	'third_party/crc32c' \
	'third_party/cros_system_api' \
	'third_party/devscripts' \
	'third_party/dom_distiller_js' \
	'third_party/expat' \
	'third_party/fips181' \
	'third_party/flatbuffers' \
	'third_party/flot' \
	'third_party/freetype' \
	'third_party/freetype/src' \
	'third_party/freetype/src/src' \
	'third_party/freetype/src/src/psnames' \
	'third_party/google_input_tools' \
	'third_party/google_input_tools/third_party/closure_library' \
	'third_party/google_input_tools/third_party/closure_library/third_party/closure' \
	'third_party/googletest' \
	'third_party/googletest/src' \
	'third_party/googletest/src/googletest' \
	'third_party/googletest/src/googletest/include' \
	'third_party/googletest/src/googletest/include/gtest' \
	'third_party/hunspell' \
	'third_party/iccjpeg' \
	'third_party/inspector_protocol' \
	'third_party/jinja2' \
	'third_party/jstemplate' \
	'third_party/khronos' \
	'third_party/leveldatabase' \
	'third_party/libXNVCtrl' \
	'third_party/libaddressinput' \
	'third_party/libjingle' \
	'third_party/libphonenumber' \
	'third_party/libsecret' \
	'third_party/libsrtp' \
	'third_party/libudev' \
	'third_party/libusb' \
	'third_party/libvpx' \
	'third_party/libxml/chromium' \
	'third_party/libwebm' \
	'third_party/libyuv' \
	'third_party/lss' \
	'third_party/lzma_sdk' \
	'third_party/mesa' \
	'third_party/modp_b64' \
	'third_party/mt19937ar' \
	'third_party/node' \
	'third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2' \
	'third_party/openmax_dl' \
	'third_party/opus' \
	'third_party/ots' \
	'third_party/pdfium' \
	'third_party/pdfium/third_party/agg23' \
	'third_party/pdfium/third_party/base' \
	'third_party/pdfium/third_party/bigint' \
	'third_party/pdfium/third_party/build' \
	'third_party/pdfium/third_party/freetype' \
	'third_party/pdfium/third_party/lcms' \
	'third_party/pdfium/third_party/libopenjpeg20' \
	'third_party/pdfium/third_party/libpng16' \
	'third_party/pdfium/third_party/libtiff' \
	'third_party/polymer' \
	'third_party/protobuf' \
	'third_party/protobuf/third_party/six' \
	'third_party/ply' \
	'third_party/qcms' \
	'third_party/qunit' \
	'third_party/sfntly' \
	'third_party/sinonjs' \
	'third_party/skia' \
	'third_party/skia/third_party/gif' \
	'third_party/smhasher' \
	'third_party/sqlite' \
	'third_party/tcmalloc' \
	'third_party/usrsctp' \
	'third_party/web-animations-js' \
	'third_party/webdriver' \
	'third_party/webrtc' \
	'third_party/widevine' \
	'third_party/woff2' \
	'third_party/libvpx/source/libvpx/third_party/x86inc' \
	'buildtools/third_party/libc++' \
	'url/third_party/mozilla' \
	'v8/third_party/inspector_protocol' \
	'v8/src/third_party/valgrind' \
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
myconf_gn+=" use_system_harfbuzz=true "
%endif
myconf_gn+=" use_gnome_keyring=false "
myconf_gn+=" fatal_linker_warnings=false "
myconf_gn+=" system_libdir=\"%{_lib}\""
myconf_gn+=" use_allocator=\"none\""
myconf_gn+=" use_aura=true "
myconf_gn+=" use_gconf=false"
myconf_gn+=" icu_use_data_file=true"
%if %{with gtk3}
myconf_gn+=" use_gtk3=true "
%else
myconf_gn+=" use_gtk3=false "
%endif
%if %{with ozone}
myconf_gn+=" use_ozone=true "
%endif
myconf_gn+=" enable_nacl=false "
myconf_gn+=" proprietary_codecs=true "
myconf_gn+=" ffmpeg_branding=\"ChromeOS\" "
myconf_gn+=" enable_ac3_eac3_audio_demuxing=true "
myconf_gn+=" enable_hevc_demuxing=true "
myconf_gn+=" enable_mse_mpeg2ts_stream_parser=true "
%ifarch i586
myconf_gn+=" target_cpu=\"x86\""
%endif
%ifarch x86_64
myconf_gn+=" target_cpu=\"x64\""
%endif
%ifarch %arm
myconf_gn+=" target_cpu=\"arm\""
myconf_gn+=" remove_webcore_debug_symbols=true"
myconf_gn+=" rtc_build_with_neon=true"
%endif
%ifarch aarch64
myconf_gn+=" target_cpu=\"arm64\""
%endif
myconf_gn+=" google_api_key=\"%{google_api_key}\""
myconf_gn+=" google_default_client_id=\"%{google_default_client_id}\""
myconf_gn+=" google_default_client_secret=\"%{google_default_client_secret}\""

# Set system libraries to be used
gn_system_libraries="
    flac
    opus
    libjpeg
    libwebp
    ffmpeg
    libxslt
    snappy
    yasm
"
#    libpng
# cb - chrome 58
# libevent as system lib causes some hanging issues particularly with extensions

%if %{with system_minizip}
gn_system_libraries+=" zlib"
%endif
%if %{with system_harfbuzz}
gn_system_libraries+=" harfbuzz-ng"
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
python2 build/linux/unbundle/replace_gn_files.py --system-libraries ${gn_system_libraries}

python2 tools/gn/bootstrap/bootstrap.py -v --gn-gen-args "${myconf_gn}"

python2 third_party/libaddressinput/chromium/tools/update-strings.py

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
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{name}.1 || :
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
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%optional %{_mandir}/man1/%{name}*

%files -n chromedriver
%doc LICENSE AUTHORS
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver
