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
%define	_empty_manifest_terminate_build 0

%ifarch %ix86
%define _build_pkgcheck_set %{nil}
%endif

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

# Libraries that should be unbundled
%global system_libs brotli dav1d flac ffmpeg fontconfig harfbuzz-ng icu libaom libjpeg libpng libdrm libwebp libxml libxslt opus openh264 libusb zlib libevent freetype
# FIXME add libvpx [currently results in build failure]
# re2 jsoncpp snappy <-- can't be added right now because of use_custom_libcxx=true, system libs use libstdc++
%define system() %(if echo %{system_libs} |grep -q -E '(^| )%{1}( |$)'; then echo -n 1; else echo -n 0;  fi)

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

Name: 		chromium-browser-%{channel}
# Working version numbers can be found at
# http://omahaproxy.appspot.com/
Version: 	107.0.5304.110
### Don't be evil!!! ###
%define ungoogled 107.0.5304.107-1
%define stha 107-patchset-1
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
%if ! 0%{?ungoogled:1}
# Ungoogled Chromium already builds a PIE sandbox
Patch0:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-70.0.3538.67-sandbox-pie.patch
%endif
# Use /etc/chromium for master_prefs
Patch1:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-68.0.3440.106-master-prefs-path.patch
# Use gn system files
# Do not prefix libpng functions
Patch4:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-60.0.3112.78-no-libpng-prefix.patch
# Do not mangle zlib
Patch6:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-77.0.3865.75-no-zlib-mangle.patch
# Use Gentoo's Widevine hack
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-widevine-r3.patch
Patch8:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-71.0.3578.98-widevine-r3.patch
# Try to load widevine from other places
Patch11:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-100.0.4896.60-widevine-other-locations.patch
# Add "Fedora" to the user agent string
#Patch13:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-fedora-user-agent.patch
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-unbundle-zlib.patch
Patch53:	chromium-81-unbundle-zlib.patch
# Needs to be submitted..
Patch54:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-77.0.3865.75-gcc-include-memory.patch

Patch64:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-98.0.4758.80-EnumTable-crash.patch

%if %omvver > 4050000
# only cooker has markupsafe > 2.0
Patch65: 	https://src.fedoraproject.org/rpms/chromium/raw/rawhide/f/chromium-99.0.4844.84-markdownsafe-soft_str.patch
%endif

# From Arch and Gentoo
# https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=chromium-dev
Patch101:	https://raw.githubusercontent.com/gentoo/gentoo/master/www-client/chromium/files/chromium-93-InkDropHost-crash.patch
Patch102:	https://raw.githubusercontent.com/gentoo/gentoo/master/www-client/chromium/files/chromium-shim_headers.patch
Patch103:	https://raw.githubusercontent.com/archlinux/svntogit-packages/packages/chromium/trunk/use-oauth2-client-switches-as-default.patch
Patch105:	reverse-roll-src-third_party-ffmpeg.patch

# Use lstdc++ on EPEL7 only
#Patch101:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-75.0.3770.100-epel7-stdc++.patch
# el7 only patch
#Patch102:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-79.0.3945.56-el7-noexcept.patch

# Apply these patches to work around EPEL8 issues
#Patch300:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-76.0.3809.132-rhel8-force-disable-use_gnome_keyring.patch

#Patch501:	https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-75.0.3770.80-SIOCGSTAMP.patch

### Chromium gcc/libstdc++ support ###
# https://github.com/stha09/chromium-patches
%if 0%{?stha:1}
Source500:	https://github.com/stha09/chromium-patches/releases/download/chromium-%{stha}/chromium-%{stha}.tar.xz
%endif

%if 0%{?ungoogled:1}
Source1000:	https://github.com/ungoogled-software/ungoogled-chromium/archive/%{ungoogled}.tar.gz
Patch1000:	chromium-107-fix-build-after-ungoogling.patch
%endif

### Chromium Tests Patches ###
# Arch Linux, fix for compile error with system ICU

# Enable VAAPI support on Linux
# FIXME reenable once the patchset has caught up with upstream
# https://github.com/saiarcot895/chromium-ubuntu-build

# omv
Patch1001:	chromium-64-system-curl.patch
Patch1002:	chromium-69-no-static-libstdc++.patch
Patch1003:	chromium-system-zlib.patch
Patch1004:	chromium-107-system-libs.patch
#Patch1007:	chromium-81-enable-gpu-features.patch
Patch2:		https://src.fedoraproject.org/rpms/chromium/raw/master/f/chromium-67.0.3396.62-gn-system.patch
Patch1006:	https://raw.githubusercontent.com/ungoogled-software/ungoogled-chromium-fedora/master/chromium-91.0.4472.77-java-only-allowed-in-android-builds.patch
Patch1009:	chromium-97-compilefixes.patch
Patch1010:	chromium-97-ffmpeg-4.4.1.patch
Patch1011:	chromium-99-ffmpeg-5.0.patch
Patch1013:	chromium-105-minizip-ng.patch
Patch1014:	chromium-107-ffmpeg-5.1.patch

Provides: 	%{crname}
Obsoletes: 	chromium-browser-unstable < %{EVRD}
%if "%{channel}" == "stable" || "%{channel}" == "beta"
Obsoletes: 	chromium-browser-dev < %{EVRD}
%endif
%if "%{channel}" == "stable"
Obsoletes: 	chromium-browser-beta < %{EVRD}
%endif
BuildRequires:	glibc-static-devel
BuildRequires: 	gperf
BuildRequires: 	bison
BuildRequires: 	re2c
BuildRequires: 	flex
BuildRequires:	git
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(krb5)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(com_err)
BuildRequires: 	alsa-oss-devel
BuildRequires:	atomic-devel
BuildRequires: 	snappy-devel
BuildRequires: 	jsoncpp-devel
BuildRequires: 	pkgconfig(expat)
BuildRequires: 	pkgconfig(glib-2.0)
BuildRequires: 	pkgconfig(wayland-egl)
BuildRequires: 	pkgconfig(nss)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-glx)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:	pkgconfig(dri)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(atspi-2)
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(atk-bridge-2.0)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libinput)
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	%{_lib}GL-devel
BuildRequires: 	bzip2-devel
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
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat) >= 57.41.100
BuildRequires:  pkgconfig(libavutil)
%endif
%if %{system flac}
BuildRequires: 	pkgconfig(flac)
%endif
%if %{system fontconfig}
BuildRequires: 	pkgconfig(fontconfig)
%endif
%if %{system harfbuzz-ng}
BuildRequires:	harfbuzz-devel
%endif
%if %{system icu}
BuildRequires:  pkgconfig(icu-i18n)
%endif
%if %{system libaom}
BuildRequires:	pkgconfig(aom)
%endif
%if %{system libdrm}
BuildRequires:	pkgconfig(libdrm)
%endif
%if %{system libevent}
BuildRequires: 	pkgconfig(libevent)
%endif
%if %{system libjpeg}
BuildRequires: 	jpeg-devel
%endif
%if %{system libpng}
BuildRequires: 	pkgconfig(libpng)
%endif
%if %{system libusb}
BuildRequires: 	pkgconfig(libusb-1.0)
%endif
%if %{system libvpx}
BuildRequires: 	pkgconfig(vpx)
%endif
%if %{system libwebp}
BuildRequires: 	pkgconfig(libwebp)
%endif
%if %{system libxml}
BuildRequires: 	pkgconfig(libxml-2.0)
%endif
%if %{system libxslt}
BuildRequires: 	pkgconfig(libxslt)
%endif
%if %{system opus}
BuildRequires: 	pkgconfig(opus)
%endif
%if %{system openh264}
BuildRequires:	pkgconfig(openh264)
%endif
%if %{system re2}
BuildRequires:	pkgconfig(re2)
%endif
%if %{system zlib}
BuildRequires: 	pkgconfig(zlib)
BuildRequires: 	pkgconfig(minizip)
%endif
BuildRequires: 	pkgconfig(nspr)
BuildRequires: 	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xshmfence)
BuildRequires: 	pkgconfig(glu)
BuildRequires: 	pkgconfig(gl)
BuildRequires: 	cups-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires: 	pkgconfig(gnome-keyring-1)
BuildRequires: 	pam-devel
BuildRequires: 	pkgconfig(xtst)
BuildRequires: 	pkgconfig(libpulse)
BuildRequires: 	pkgconfig(xt)
BuildRequires: 	cap-devel
BuildRequires: 	elfutils-devel
BuildRequires: 	pkgconfig(gnutls)
BuildRequires: 	pkgconfig(udev)
BuildRequires: 	pkgconfig(speex)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(snappy)

BuildRequires:	pkgconfig(python)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:	python%{pyver}dist(protobuf)
BuildRequires:  python%{pyver}dist(markupsafe)

BuildRequires: 	yasm
BuildRequires:  speech-dispatcher-devel
BuildRequires:  pkgconfig(libpci)
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
# Not using %%autosetup so we can apply patches after stha09 and
# ungoogled-chromium patches have been applied
%setup -q -n chromium-%{version} %{?stha:-a 500} %{?ungoogled:-a 1000}
%if 0%{?stha:1}
j=1
for i in patches/*; do
	if basename $i |grep -qE '~$'; then continue; fi
	echo "Applying `basename $i`"
	patch -p1 -z .stha09-${j}~ -b <$i
	j=$((j+1))
done
%endif

%if 0%{?ungoogled:1}
UGDIR=$(pwd)/ungoogled-chromium-%{ungoogled}
echo %{version} >$UGDIR/chromium_version.txt
# FIXME we shouldn't un-prune anything, but this seems to be needed
sed -i -e '/esbuild/d' $UGDIR/pruning.list
python $UGDIR/utils/prune_binaries.py ./ $UGDIR/pruning.list
python $UGDIR/utils/patches.py apply ./ $UGDIR/patches
python $UGDIR/utils/domain_substitution.py apply -r $UGDIR/domain_regex.list -f $UGDIR/domain_substitution.list -c domainsubcache.tar.gz ./
%endif

%autopatch -p1

rm -rf third_party/binutils/

echo "%{revision}" > build/LASTCHANGE.in

sed -i 's!-nostdlib++!!g'  build/config/posix/BUILD.gn
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

#if %omvver <= 4050000
# Look, I don't know. This package is spit and chewing gum. Sorry.
rm -rf third_party/markupsafe
ln -s %{python3_sitearch}/markupsafe third_party/markupsafe
# We should look on removing other python packages as well i.e. ply
#endif

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
%ifarch x86_64
# Not needed for znver1, and shouldn't be used for x86_64, but
# is needed right now
# https://file-store.openmandriva.org/api/v1/file_stores/98a2f814bb2fcd7821643aac55d678ba74aff510.log?show=true
%global optflags %{optflags} -mbmi2
%endif

export CC=clang
export CXX=clang++

_lto_cpus="$(getconf _NPROCESSORS_ONLN)"
if [ $_lto_cpus -gt 4 ]; then
	# LTO is very memory intensive, so
	# 32 parallel LTO jobs may not be
	# a good idea...
	_lto_cpus=4
fi

GN_DEFINES=""
%if 0%{?ungoogled:1}
GN_DEFINES+=" $(cat $UGDIR/flags.gn |tr '\n' ' ')"
%endif
GN_DEFINES+="use_sysroot=false is_debug=false fieldtrial_testing_like_official_build=true "
GN_DEFINES+=" is_clang=true clang_base_path=\"%{_prefix}\" clang_use_chrome_plugins=false "
GN_DEFINES+=" treat_warnings_as_errors=false "
%if 1
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
GN_DEFINES+=" use_gtk=false use_qt=true "
if ! echo %{system_libs} |grep -q icu; then
GN_DEFINES+=" icu_use_data_file=true"
fi
GN_DEFINES+=" use_gnome_keyring=false "
GN_DEFINES+=" fatal_linker_warnings=false "
GN_DEFINES+=" system_libdir=\"%{_lib}\""
GN_DEFINES+=" use_allocator=\"none\""
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
GN_DEFINES+=" thin_lto_enable_optimizations=true use_clang=true use_lld=true use_thin_lto=true"
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
GN_DEFINES+=" enable_hevc_parser_and_hw_decoder=true enable_jxl_decoder=true"
GN_DEFINES+=" enable_media_drm_storage=true"
%ifarch %{x86_64}
GN_DEFINES+=" enable_perfetto_x64_cpu_opt=true"
%endif
GN_DEFINES+=" enable_precompiled_headers=true"
GN_DEFINES+=" is_official_build=true"
GN_DEFINES+=" ozone_platform_drm=true"
GN_DEFINES+=" perfetto_use_system_zlib=true"
GN_DEFINES+=" rtc_link_pipewire=true rtc_use_pipewire=true"
GN_DEFINES+=" use_libinput=true use_real_dbus_clients=true"
GN_DEFINES+=" use_vaapi_image_codecs=true"
# 107: Build failure: GN_DEFINES+=" enable_wayland_server=true"
# 107: Build failure: GN_DEFINES+=" perfetto_use_system_protobuf=true"
# 107: Build failure: GN_DEFINES+=" use_v4l2_codec=true use_v4lplugin=true"
# 107: Build failure: GN_DEFINES+=" use_webaudio_ffmpeg=true"

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

python tools/gn/bootstrap/bootstrap.py --skip-generate-buildfiles

python third_party/libaddressinput/chromium/tools/update-strings.py

out/Release/gn gen --script-executable=/usr/bin/python --args="${GN_DEFINES}" out/Release

%ifarch %{x86_64}
ninja -C out/Release chrome chrome_sandbox chromedriver
%else
ninja -C out/Release chrome chrome_sandbox
%endif

%install
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

%ifarch %{x86_64}
%files -n chromedriver%{namesuffix}
%doc LICENSE AUTHORS
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver
%endif
