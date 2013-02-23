%define crname chromium-browser
%define _crdir %{_libdir}/%{crname}
%define _src %{_topdir}/SOURCES

Name: chromium-browser-stable
Version: 25.0.1364.97
Release:  1
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL

Source0: http://download.rfremix.ru/storage/chromium/%{version}/chromium-%{version}.tar.xz
Source1: chromium-wrapper
Source30: master_preferences
Source31: default_bookmarks.html
Source2: chromium-browser.desktop
Source100: icons.tar.bz2
Patch0: chromium-21.0.1171.0-remove-inline.patch
Patch4: chromium-20.0.1132.47-master-prefs-path.patch
Patch5:	chromium-26.0.1368.0-glib-2.16-use-siginfo_t.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Provides: %{crname}
Conflicts: chromium-browser-unstable
Conflicts: chromium-browser-beta
Obsoletes: chromium-browser < 1:9.0.597.94
BuildRequires: bison, flex, gtk2-devel, atk-devel, pkgconfig(expat), gperf
BuildRequires: nspr-devel, nss-devel, libalsa-devel, util-linux
BuildRequires: glib2-devel, bzip2-devel, zlib-devel, png-devel
BuildRequires: jpeg-devel, mesagl-devel, mesaglu-devel
BuildRequires: libxscrnsaver-devel, dbus-glib-devel, cups-devel
BuildRequires: libgnome-keyring-devel libvpx-devel libxtst-devel
BuildRequires: libxslt-devel libxml2-devel libxt-devel pam-devel
BuildRequires: libevent-devel libflac-devel pulseaudio-devel
BuildRequires: elfutils-devel udev-devel speex-devel yasm
ExclusiveArch: i586 x86_64 armv7l

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
%setup -q -n chromium-%{version}
%patch0 -p1 -b .remove-inline
%patch4 -p1 -b .prefs
%patch5 -p0 -b .siginfo~

# Hard code extra version
FILE=chrome/common/chrome_version_info_posix.cc
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
	-D use_system_libxml=0 \
	-D use_system_zlib=0 \
	-D use_system_bzip2=1 \
	-D use_system_xdg_utils=1 \
	-D use_system_yasm=1 \
	-D use_system_libpng=1 \
	-D use_system_libjpeg=1 \
	-D use_system_libevent=1 \
	-D use_system_speex=1 \
	-D use_system_flac=1 \
	-D use_system_vpx=0 \
	-D use_system_icu=0 \
%ifarch i586
	-D disable_sse2=1 \
	-D release_extra_cflags="-march=i586"
%endif
%ifarch armv7l
	-D target_arch=arm \
	-D disable_nacl=1 \
	-D linux_use_tcmalloc=0 \
	-D armv7=1 \
	-D release_extra_cflags="-marm"
%endif

# Note: DON'T use system sqlite (3.7.3) -- it breaks history search

%make chrome chrome_sandbox BUILDTYPE=Release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_crdir}/locales
mkdir -p %{buildroot}%{_crdir}/themes
mkdir -p %{buildroot}%{_crdir}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{_src}/chromium-wrapper %{buildroot}%{_crdir}/
install -m 755 out/Release/chrome %{buildroot}%{_crdir}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_crdir}/chrome-sandbox
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{crname}.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_crdir}/

install -m 644 out/Release/chrome_100_percent.pak %{buildroot}%{_crdir}/
install -m 644 out/Release/content_resources.pak %{buildroot}%{_crdir}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_crdir}/
%ifnarch armv7l
install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{_crdir}/
install -m 755 out/Release/nacl_helper %{buildroot}%{_crdir}/
install -m 644 out/Release/nacl_irt_*.nexe %{buildroot}%{_crdir}/
%endif
install -m 644 out/Release/locales/*.pak %{buildroot}%{_crdir}/locales/
#install -m 755 out/Release/xdg-mime %{buildroot}%{_crdir}/
#install -m 755 out/Release/xdg-settings %{buildroot}%{_crdir}/
install -m 644 out/Release/resources.pak %{buildroot}%{_crdir}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_crdir}/default_apps/
ln -s %{_crdir}/chromium-wrapper %{buildroot}%{_bindir}/%{crname}

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_crdir}

# Strip NaCl IRT
%ifarch x86_64
./native_client/toolchain/linux_x86_newlib/bin/x86_64-nacl-strip %{buildroot}%{_crdir}/nacl_irt_x86_64.nexe
%endif
%ifarch i586
./native_client/toolchain/linux_x86_newlib/bin/i686-nacl-strip %{buildroot}%{_crdir}/nacl_irt_x86_32.nexe
%endif

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{_src}/%{crname}.desktop %{buildroot}%{_datadir}/applications/

# icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/
tar xjf %{SOURCE100} -C %{buildroot}%{_iconsdir}/hicolor/

mkdir -p %{buildroot}%{_sysconfdir}/%{crname}
install -m 0644 %{SOURCE30} %{buildroot}%{_sysconfdir}/%{crname}/
install -m 0644 %{SOURCE31} %{buildroot}%{_sysconfdir}/%{crname}/

find %{buildroot} -name "*.nexe" -exec strip {} \;

%clean
rm -rf %{buildroot}

%files -n chromium-browser

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/%{crname}
%{_bindir}/%{crname}
%{_crdir}/chromium-wrapper
%{_crdir}/chrome
%{_crdir}/chrome-sandbox
%{_crdir}/chrome.pak
%{_crdir}/libffmpegsumo.so
%ifnarch armv7l
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


%changelog
* Sun Dec  2 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 23.0.1271.95-1
- update to 23.0.1271.95

* Wed Nov 27 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 23.0.1271.91-1
- update to 23.0.1271.91

* Thu Nov 22 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 23.0.1271.64-2
- apply new icons

* Tue Nov 20 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 23.0.1271.64-1
- update to 23.0.1271.64-1

* Mon Oct 22 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 22.0.1229.92-2
- build with internal libxml to avoid (rosa#1008)

* Tue Oct  9 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 22.0.1229.92-1
- update to 22.0.1229.92
- fix config

* Thu Sep 27 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 22.0.1229.79-1
- update to 22.0.1229.79
- new home page

* Thu Sep 20 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 21.0.1180.89-1
- update to 21.0.1180.89

* Thu Aug  9 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 21.0.1180.75-1
- update to 21.0.1180.75

* Fri Aug  3 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 21.0.1180.57-1
- update to 21.0.1180.57
- drop old patches

* Tue Jul 24 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 20.0.1132.57-4
- drop some patches for ROSA LTS

* Tue Jul 24 2012 Arkady L. Shane <arkady.shane@rosalab.ru> 20.0.1132.57-3
- apply patch to build on gcc 4.7
- apply memory leak sqlite patch

* Fri Jul 13 2012 Claudio Matsuoka <claudio@mandriva.com> 20.0.1132.57-2mdv2011.0
+ Revision: 809196
- add missing standard theme resources

* Thu Jul 12 2012 Claudio Matsuoka <claudio@mandriva.com> 20.0.1132.57-1
+ Revision: 809041
- new upstream release 20.0.1132.57 (145807)
  * [129898] High CVE-2012-2842: Use-after-free in counter handling
  * [130595] High CVE-2012-2843: Use-after-free in layout height tracking
  * [133450] High CVE-2012-2844: Bad object access with JavaScript in PDF
- use system yasm, flac and speex

* Wed Jul 04 2012 Claudio Matsuoka <claudio@mandriva.com> 20.0.1132.47-2
+ Revision: 808143
- new upstream release 20.0.1132.47 (144678)

* Tue Jul 03 2012 Claudio Matsuoka <claudio@mandriva.com> 20.0.1132.47-1
+ Revision: 807999
- new upstream release 20.0.1132.43 (135598)
  * [118633] Low CVE-2012-2815: Leak of iframe fragment id.
  * [120222] High CVE-2012-2817: Use-after-free in table section handling.
  * [120944] High CVE-2012-2818: Use-after-free in counter layout.
  * [120977] High CVE-2012-2819: Crash in texture handling.
  * [121926] Medium CVE-2012-2820: Out-of-bounds read in SVG filter handling.
  * [122925] Medium CVE-2012-2821: Autofill display problem.
  * [various] Medium CVE-2012-2822: Misc. lower severity OOB read issues in PDF.
  * [124356] High CVE-2012-2823: Use-after-free in SVG resource handling.
  * [125374] High CVE-2012-2824: Use-after-free in SVG painting.
  * [128688] Medium CVE-2012-2826: Out-of-bounds read in texture conversion.
  * [129857] High CVE-2012-2828: Integer overflows in PDF.
  * [129947] High CVE-2012-2829: Use-after-free in first-letter handling.
  * [129951] High CVE-2012-2830: Wild pointer in array value setting.
  * [130356] High CVE-2012-2831: Use-after-free in SVG reference handling.
  * [131553] High CVE-2012-2832: Uninitialized pointer in PDF image codec.
  * [132156] High CVE-2012-2833: Buffer overflow in PDF JS API.
  * [132779] High CVE-2012-2834: Integer overflow in Matroska container.
  * [127417] Medium CVE-2012-2825: Wild read in XSL handling.
  * [64-bit Linux only] [129930] High CVE-2012-2807: Integer overflows in
    libxml.

* Wed Jun 20 2012 Claudio Matsuoka <claudio@mandriva.com> 19.0.1084.56-1
+ Revision: 806474
- new upstream release 19.0.1084.56 (140965)
- use system xdg utils
- strip debug from NaCl IRT files
- new upstream release 19.0.1084.52 (138391)
- new upstream release 19.0.1084.41 (134854)
- move chromium 19 from beta to stable
- remove chromium 18
- fix pulseaudio-devel dependency package name
- requires libudev devel
- new upstream release 18.0.1025.168 (134367)
  * [106413] High CVE-2011-3078: Use after free in floats handling
  * [117110] High CVE-2012-1521: Use after free in xml parser
  * [117627] Medium CVE-2011-3079: IPC validation failure
  * [121726] Medium CVE-2011-3080: Race condition in sandbox IPC
  * [121899] High CVE-2011-3081: Use after free in floats handling
- new upstream release 18.0.1025.162 (131933)
- new upstream release 18.0.1025.151 (130497)
  * fix black screen on Hybrid Graphics system with GPU accelerated
    compositing enabled (Issue: 117371)
  * fix CSS not applied to <content> element (Issue: 114667)
  * fix Regression rendering a div with background gradient and borders
    (Issue: 113726)
  * fix Canvas 2D line drawing bug with GPU acceleration (Issue: 121285)
  * fix Multiple crashes (Issues: 72235, 116825 and 92998)
  * fix Pop-up dialog is at wrong position (Issue: 116045)
  * fix HTML Canvas patterns are broken if you change the transformation
    matrix (Issue: 112165)
  * fix SSL interstitial error "proceed anyway" / "back to safety" buttons
    don't work (Issue: 119252)
  * [106577] Medium CVE-2011-3066: Out-of-bounds read in Skia clipping
  * [117583] Medium CVE-2011-3067: Cross-origin iframe replacement
  * [117698] High CVE-2011-3068: Use-after-free in run-in handling
  * [117728] High CVE-2011-3069: Use-after-free in line box handling
  * [118185] High CVE-2011-3070: Use-after-free in v8 bindings
  * [118273] High CVE-2011-3071: Use-after-free in HTMLMediaElement
  * [118467] Low CVE-2011-3072: Cross-origin violation parenting pop-up window
  * [118593] High CVE-2011-3073: Use-after-free in SVG resource handling
  * [119281] Medium CVE-2011-3074: Use-after-free in media handling
  * [119525] High CVE-2011-3075: Use-after-free applying style command
  * [120037] High CVE-2011-3076: Use-after-free in focus handling
  * [120189] Medium CVE-2011-3077: Read-after-free in script bindings
- new upstream release 18.0.1025.142
  * [109574] Medium CVE-2011-3058: Bad interaction possibly leading to XSS
    in EUC-JP
  * [112317] Medium CVE-2011-3059: Out-of-bounds read in SVG text handling
  * [114056] Medium CVE-2011-3060: Out-of-bounds read in text fragment handling
  * [116398] Medium CVE-2011-3061: SPDY proxy certificate checking error
  * [116524] High CVE-2011-3062: Off-by-one in OpenType Sanitizer
  * [117417] Low CVE-2011-3063: Validate navigation requests from the renderer
    more carefully
  * [117471] High CVE-2011-3064: Use-after-free in SVG clipping
  * [117588] High CVE-2011-3065: Memory corruption in Skia
  * [117794] Medium CVE-2011-3057: Invalid read in v8
- new upstream release 18.0.1025.113
- move chromium 18 from beta to stable
- remove chromium 17
- new upstream release 17.0.963.65 (124586)
- move chromium 17 from beta to stable

* Thu Jan 26 2012 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.77-1
+ Revision: 769167
- fix required package names
- new upstream release 16.0.912.77 (118311)
  * [106484] High CVE-2011-3924: Use-after-free in DOM selections
  * [107182] Critical CVE-2011-3925: Use-after-free in Safe Browsing navigation
  * [108461] High CVE-2011-3928: Use-after-free in DOM handling
  * [108605] High CVE-2011-3927: Uninitialized value in Skia
  * [109556] High CVE-2011-3926: Heap-buffer-overflow in tree builder

* Fri Jan 06 2012 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.75-1
+ Revision: 758280
- new upstream release 16.0.912.75 (116452)
  * [106672] High CVE-2011-3921: Use-after-free in animation frames.
  * [107128] High CVE-2011-3919: Heap-buffer-overflow in libxml.
  * [108006] High CVE-2011-3922: Stack-buffer-overflow in glyph handling.
- detailed changelog: http://goo.gl/n2A6J

* Wed Dec 14 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.63-1
+ Revision: 741173
- fix libxt-devel package name in requires
- fix cups-devel package name in requires
- new upstream release 16.0.912.63 (113337)
- security fixes
  * [81753] Medium CVE-2011-3903: Out-of-bounds read in regex matching.
  * [95465] Low CVE-2011-3905: Out-of-bounds reads in libxml.
  * [98809] Medium CVE-2011-3906: Out-of-bounds read in PDF parser.
  * [99016] High CVE-2011-3907: URL bar spoofing with view-source.
  * [100863] Low CVE-2011-3908: Out-of-bounds read in SVG parsing.
  * [101010] Medium CVE-2011-3909: [64-bit only] Memory corruption in CSS
    property array.
  * [101494] Medium CVE-2011-3910: Out-of-bounds read in YUV video frame
    handling.
  * [101779] Medium CVE-2011-3911: Out-of-bounds read in PDF.
  * [102359] High CVE-2011-3912: Use-after-free in SVG filters.
  * [103921] High CVE-2011-3913: Use-after-free in Range handling.
  * [104011] High CVE-2011-3914: Out-of-bounds write in v8 i18n handling.
  * [104529] High CVE-2011-3915: Buffer overflow in PDF font handling.
  * [104959] Medium CVE-2011-3916: Out-of-bounds reads in PDF cross references.
  * [105162] Medium CVE-2011-3917: Stack-buffer-overflow in FileWatcher.
  * [107258] High CVE-2011-3904: Use-after-free in bidi handling.
- move chromium 16 to stable
- fix elfutils-devel package name in requires

* Sat Nov 12 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.120-1
+ Revision: 730285
- only include glib.h directly

* Wed Oct 26 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.106-1
+ Revision: 707420
- new upstream release 15.0.874.106 (107270)
  * fixes login issues to Barrons Online and The Wall Street Journal

* Tue Oct 25 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.102-1
+ Revision: 707191
- new upstream release 15.0.874.102 (106587)
  * [86758] High CVE-2011-2845: URL bar spoof in history handling.
  * [88949] Medium CVE-2011-3875: URL bar spoof with drag+drop of URLs.
  * [90217] Low CVE-2011-3876: Avoid stripping whitespace at the end of
    download filenames.
  * [91218] Low CVE-2011-3877: XSS in appcache internals page.
  * [94487] Medium CVE-2011-3878: Race condition in worker process
    initialization.
  * [95374] Low CVE-2011-3879: Avoid redirect to chrome scheme URIs.
  * [95992] Low CVE-2011-3880: Don't permit as a HTTP header delimiter.
  * [96047][96885][98053][99512][99750] High CVE-2011-3881: Cross-origin
    policy violations.
  * [96292] High CVE-2011-3882: Use-after-free in media buffer handling.
  * [96902] High CVE-2011-3883: Use-after-free in counter handling.
  * [97148] High CVE-2011-3884: Timing issues in DOM traversal.
  * [97599][98064][98556][99294][99880][100059] High CVE-2011-3885: Stale
    style bugs leading to use-after-free.
  * [98773][99167] High CVE-2011-3886: Out of bounds writes in v8.
  * [98407] Medium CVE-2011-3887: Cookie theft with javascript URIs.
  * [99138] High CVE-2011-3888: Use-after-free with plug-in and editing.
  * [99211] High CVE-2011-3889: Heap overflow in Web Audio.
  * [99553] High CVE-2011-3890: Use-after-free in video source handling.
  * [100332] High CVE-2011-3891: Exposure of internal v8 functions.
- move Chromium 15 from beta to stable
- remove Chromium 14
- add support to armv7l
- new upstream release 14.0.835.202 (103287)
- security fixes:
  * [93788] High CVE-2011-2876: Use-after-free in text line box handling
  * [95072] High CVE-2011-2877: Stale font in SVG text handling
  * [95671] High CVE-2011-2878: Inappropriate cross-origin access to the
    window prototype
  * [96150] High CVE-2011-2879: Lifetime and threading issues in audio node
    handling
  * [97451] [97520] [97615] High CVE-2011-2880: Use-after-free in the v8
    bindings
  * [97784] High CVE-2011-2881: Memory corruption with v8 hidden objects
  * [98089] Critical CVE-2011-3873: Memory corruption in shader translator
- detailed changelog at http://goo.gl/4dBM1
- new upstream release 14.0.835.186 (101821)

* Sat Sep 17 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.163-1
+ Revision: 700172
- new upstream release 14.0.835.163 (101024)
- security fixes:
  * [49377] High CVE-2011-2835: Race condition in the certificate cache
  * [57908] Low CVE-2011-2837: Use PIC / pie compiler flags
  * [75070] Low CVE-2011-2838: Treat MIME type more authoritatively when
    loading plug-ins
  * [76771] High CVE-2011-2839: Crash in v8 script object wrappers
  * [78427] [83031] Low CVE-2011-2840: Possible URL bar spoofs with unusual
    user interaction
  * [78639] High CVE-2011-2841: Garbage collection error in PDF
  * [82438] Medium CVE-2011-2843: Out-of-bounds read with media buffers
  * [85041] Medium CVE-2011-2844: Out-of-bounds read with mp3 files
  * [$1000] [89219] High CVE-2011-2846: Use-after-free in unload event handling
  * [$1000] [89330] High CVE-2011-2847: Use-after-free in document loader
  * [89564] Medium CVE-2011-2848: URL bar spoof with forward button
  * [89795] Low CVE-2011-2849: Browser NULL pointer crash with WebSockets
  * [89991] Medium CVE-2011-3234: Out-of-bounds read in box handling
  * [90134] Medium CVE-2011-2850: Out-of-bounds read with Khmer characters
  * [90173] Medium CVE-2011-2851: Out-of-bounds read in video handling
  * [91120] High CVE-2011-2852: Off-by-one in v8
  * [91197] High CVE-2011-2853: Use-after-free in plug-in handling
  * [92651] [94800] High CVE-2011-2854: Use-after-free in ruby / table style
    handing
  * [92959] High CVE-2011-2855: Stale node in stylesheet handling
  * [93416] High CVE-2011-2856: Cross-origin bypass in v8
  * [93420] High CVE-2011-2857: Use-after-free in focus controller
  * [93472] High CVE-2011-2834: Double free in libxml XPath handling
  * [93497] Medium CVE-2011-2859: Incorrect permissions assigned to
    non-gallery pages
  * [93587] High CVE-2011-2860: Use-after-free in table style handling
  * [93596] Medium CVE-2011-2861: Bad string read in PDF
  * [93906] High CVE-2011-2862: Unintended access to v8 built-in objects
  * [95563] Medium CVE-2011-2864: Out-of-bounds read with Tibetan characters
  * [95625] Medium CVE-2011-2858: Out-of-bounds read with triangle arrays
  * [95917] Low CVE-2011-2874: Failure to pin a self-signed cert for a session
  * [95920] High CVE-2011-2875: Type confusion in v8 object sealing
- detailed changelog at http://goo.gl/6B1kT
- copy release 14.0.835.163 from beta to stable

* Sun Sep 04 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.220-1
+ Revision: 698257
- new upstream release 13.0.782.220 (99552)
  * revoking trust for SSL certificates issued by DigiNotar-controlled
    intermediate CAs used by the Dutch PKIoverheid program

* Tue Aug 23 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.215-1
+ Revision: 696339
- add fix for tcmalloc build in cooker
- new upstream release 13.0.782.215 (97094)
- security fixes:
  * [82552] High CVE-2011-2823: Use-after-free in line box handling
  * [88216] High CVE-2011-2824: Use-after-free with counter nodes
  * [88670] High CVE-2011-2825: Use-after-free with custom fonts
  * [89402] High CVE-2011-2821: Double free in libxml XPath handling
  * [87453] High CVE-2011-2826: Cross-origin violation with empty origins
  * [90668] High CVE-2011-2827: Use-after-free in text searching
  * [91517] High CVE-2011-2828: Out-of-bounds write in v8
  * [32-bit only] [91598] High CVE-2011-2829: Integer overflow in uniform
    arrays
- detailed changelog at http://goo.gl/Lzn1m
- new upstream release 13.0.782.112 (95650)
- move release 13.0.782.107 (94237) from beta to stable
- security fixes:
  * [78841] High CVE-2011-2359: Stale pointer due to bad line box tracking
    in rendering.
  * [79266] Low CVE-2011-2360: Potential bypass of dangerous file prompt.
  * [79426] Low CVE-2011-2361: Improve designation of strings in the basic
    auth dialog.
  * [81307] Medium CVE-2011-2782: File permissions error with drag and drop.
  * [83273] Medium CVE-2011-2783: Always confirm a developer mode NPAPI
    extension install via a browser dialog.
  * [83841] Low CVE-2011-2784: Local file path disclosure via GL program log.
  * [84402] Low CVE-2011-2785: Sanitize the homepage URL in extensions.
  * [84600] Low CVE-2011-2786: Make sure the speech input bubble is always
    on-screen.
  * [84805] Medium CVE-2011-2787: Browser crash due to GPU lock re-entrancy
    issue.
  * [85559] Low CVE-2011-2788: Buffer overflow in inspector serialization.
  * [85808] Medium CVE-2011-2789: Use after free in Pepper plug-in
    instantiation.
  * [86502] High CVE-2011-2790: Use-after-free with floating styles.
  * [86900] High CVE-2011-2791: Out-of-bounds write in ICU.
  * [87148] High CVE-2011-2792: Use-after-free with float removal.
  * [87227] High CVE-2011-2793: Use-after-free in media selectors.
  * [87298] Medium CVE-2011-2794: Out-of-bounds read in text iteration.
  * [87339] Medium CVE-2011-2795: Cross-frame function leak.
  * [87548] High CVE-2011-2796: Use-after-free in Skia.
  * [87729] High CVE-2011-2797: Use-after-free in resource caching.
  * [87815] Low CVE-2011-2798: Prevent a couple of internal schemes from
    being web accessible.
  * [87925] High CVE-2011-2799: Use-after-free in HTML range handling.
  * [88337] Medium CVE-2011-2800: Leak of client-side redirect target.
  * [88591] High CVE-2011-2802: v8 crash with const lookups.
  * [88827] Medium CVE-2011-2803: Out-of-bounds read in Skia paths.
  * [88846] High CVE-2011-2801: Use-after-free in frame loader.
  * [88889] High CVE-2011-2818: Use-after-free in display box rendering.
  * [89142] High CVE-2011-2804: PDF crash with nested functions.
  * [89520] High CVE-2011-2805: Cross-origin script injection.
  * [90222] High CVE-2011-2819: Cross-origin violation in base URI handling.
- detailed changelog at http://goo.gl/25VH4

* Fri Jul 29 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.124-1
+ Revision: 692282
- new upstream release 112-12.0.742.124 (92024)

* Tue Jun 28 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.112-1
+ Revision: 687931
- new upstream release 12.0.742.112 (90785)
- security fixes:
  * [77493] Medium CVE-2011-2345: Out-of-bounds read in NPAPI string handling.
  * [84355] High CVE-2011-2346: Use-after-free in SVG font handling.
  * [85003] High CVE-2011-2347: Memory corruption in CSS parsing.
  * [85102] High CVE-2011-2350: Lifetime and re-entrancy issues in the HTML
    parser.
  * [85177] High CVE-2011-2348: Bad bounds check in v8.
  * [85211] High CVE-2011-2351: Use-after-free with SVG use element.
  * [85418] High CVE-2011-2349: Use-after-free in text selection.
- detailed changelog at http://goo.gl/PPBY4

* Tue Jun 07 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.91-1
+ Revision: 683117
- new upstream release 12.0.742.91 (stable)
  * Hardware accelerated 3D CSS
  * New Safe Browsing protection against downloading malicious files
  * Ability to delete Flash cookies from inside Chrome
  * Launch Apps by name from the Omnibox
  * Integrated Sync into new settings pages
  * Improved screen reader support
  * New warning when hitting Command-Q on Mac
  * Removal of Google Gears
- security fixes
  * [73962] [79746] High CVE-2011-1808: Use-after-free due to integer issues
    in float handling
  * [75496] Medium CVE-2011-1809: Use-after-free in accessibility support
  * [75643] Low CVE-2011-1810: Visit history information leak in CSS
  * [76034] Low CVE-2011-1811: Browser crash with lots of form submissions
  * [77026] Medium CVE-2011-1812: Extensions permission bypass
  * [78516] High CVE-2011-1813: Stale pointer in extension framework
  * [79362] Medium CVE-2011-1814: Read from uninitialized pointer
  * [79862] Low CVE-2011-1815: Extension script injection into new tab page
  * [80358] Medium CVE-2011-1816: Use-after-free in developer tools
  * [81916] Medium CVE-2011-1817: Browser memory corruption in history
    deletion
  * [81949] High CVE-2011-1818: Use-after-free in image loader
  * [83010] Medium CVE-2011-1819: Extension injection into chrome:// pages
  * [83275] High CVE-2011-2332: Same origin bypass in v8
  * [83743] High CVE-2011-2342: Same origin bypass in DOM
- copy release 12.0.742.91 from beta to stable

* Wed May 25 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.71-1
+ Revision: 678989
- new upstream release 11.0.696.71 (stable)
- security fixes
  * [72189] Low CVE-2011-1801: Pop-up blocker bypass.
  * [$1000] [82546] High CVE-2011-1804: Stale pointer in floats rendering.
  * [82873] Critical CVE-2011-1806: Memory corruption in GPU command buffer.
  * [82903] Critical CVE-2011-1807: Out-of-bounds write in blob handling.
- bug fixes
  * REGRESSION: selection extended by arrow keys flickers on LinkedIn.com.
    (Issue 83197).
  * Have ConnectBackupJob try IPv4 first to hide potential long IPv6 connect
    timeout (Issue 81686).

* Thu May 12 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.68-1
+ Revision: 673982
- new upstream release 11.0.696.68 (stable)
- security fixes
  * [64046] High CVE-2011-1799: Bad casts in Chromium WebKit glue.
  * [80608] High CVE-2011-1800: Integer overflows in SVG filters.

* Sat May 07 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.65-1
+ Revision: 671613
- new upstream release 11.0.696.65 (stable)
  * fix issue 80580: After deleting bookmarks on the Bookmark managers,
    the bookmark bar doesn't display properly with existing bookmarks.

* Fri Apr 29 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.57-1
+ Revision: 660171
- new upstream release 11.0.696.57 (stable)
- security fixes:
  * [61502] High CVE-2011-1303: Stale pointer in floating object handling
  * [70538] Low CVE-2011-1304: Pop-up block bypass via plug-ins
  * [70589] Medium CVE-2011-1305: Linked-list race in database handling
  * [71586] Medium CVE-2011-1434: Lack of thread safety in MIME handling
  * [72523] Medium CVE-2011-1435: Bad extension with tabs permission can
    capture local files
  * [72910] Low CVE-2011-1436: Possible browser crash due to bad interaction
    with X
  * [73526] High CVE-2011-1437: Integer overflows in float rendering
  * [74653] High CVE-2011-1438: Same origin policy violation with blobs
  * [74763] High CVE-2011-1439: Prevent interference between renderer
    processes
  * [75186] High CVE-2011-1440: Use-after-free with <ruby> tag and CSS
  * [75347] High CVE-2011-1441: Bad cast with floating select lists
  * [75801] High CVE-2011-1442: Corrupt node trees with mutation events
  * [76001] High CVE-2011-1443: Stale pointers in layering code
  * [76542] High CVE-2011-1444: Race condition in sandbox launcher
  * [76646] Medium CVE-2011-1445: Out-of-bounds read in SVG
  * [76666] [77507] [78031] High CVE-2011-1446: Possible URL bar spoofs with
    navigation errors and interrupted loads
  * [76966] High CVE-2011-1447: Stale pointer in drop-down list handling
  * [77130] High CVE-2011-1448: Stale pointer in height calculations
  * [77346] High CVE-2011-1449: Use-after-free in WebSockets
  * [77349] Low CVE-2011-1450: Dangling pointers in file dialogs
  * [77463] High CVE-2011-1451: Dangling pointers in DOM id map
  * [77786] Medium CVE-2011-1452: URL bar spoof with redirect and manual
    reload
  * [79199] High CVE-2011-1454: Use-after-free in DOM id handling
  * [79361] Medium CVE-2011-1455: Out-of-bounds read with multipart-encoded
    PDF
  * [79364] High CVE-2011-1456: Stale pointers with PDF forms
- detailed changelog at http://goo.gl/arI9m
- copy Chromium 11 sources from beta to stable
- remove Chromium 10 source files

* Fri Apr 15 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.205-1
+ Revision: 653084
- new upstream release 10.0.648.205 (stable)
  * Fix issue 75629: CVE-2011-1301: Use-after-free in the GPU process
  * Fix issue 78524: CVE-2011-1302: Heap overflow in the GPU process
- detailed changelog at http://goo.gl/wJg8b

* Mon Apr 04 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.204-2
+ Revision: 650370
- update chromium-browser package group
- bump release for buildsystem debug

* Fri Mar 25 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.204-1
+ Revision: 648498
- new upstream release 10.0.648.204 (stable)
  * support for password manager
  * performance and stability fixes
  * fix CVE-2011-1291: Buffer error in base string handling
  * fix CVE-2011-1292: Use-after-free in the frame loader
  * fix CVE-2011-1293: Use-after-free in HTMLCollection
  * fix CVE-2011-1294: Stale pointer in CSS handling
  * fix CVE-2011-1295: DOM tree corruption with broken node parentage
  * fix CVE-2011-1296: Stale pointer in SVG text handling
- fix some system library settings introduced in revision 647139

  + Funda Wang <fwang@mandriva.org>
    - build with more system libs

* Fri Mar 18 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.151-1
+ Revision: 646282
- new upstream release 10.0.648.151 (stable)
  * blacklist a small number of HTTPS certificates

* Sat Mar 12 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.133-1
+ Revision: 644042
- new upstream release 10.0.648.133 (stable)
  * [CVE-2011-1290] fix memory corruption in style handling
- check presence of patch files

* Fri Mar 11 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.127-2
+ Revision: 643848
- apply patches correctly

* Wed Mar 09 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.127-1
+ Revision: 643105
- new upstream release 10.0.648.127 (stable)
  * New version of V8 which greatly improves javascript performance
  * New settings pages that open in a tab, rather than a dialog box
  * Improved security with malware reporting and disabling outdated plugins
    by default
  * Password sync as part of Chrome Sync now enabled by default
  * GPU Accelerated Video
  * Background WebApps
  * webNavigation extension API
- annoucement and security fix list: http://goo.gl/PWdBi
- move chromium patch 10.0.648.114 from beta channel to stable
- move chromium patch 10.0.648.82 from beta channel to stable
- move chromium patch 10.0.648.127 from beta channel to stable
- move chromium patch 10.0.648.126 from beta channel to stable
- move chromium 10.0.648.45 from beta channel to stable
- move patch from beta channel to stable
- move patch from beta channel to stable

* Tue Mar 01 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.107-1
+ Revision: 641075
- new upstream release 9.0.597.107 (stable)
- contains security fixes, see detais at http://goo.gl/rkTSm
- add beta browser to the downgrade notice in spec description

* Sat Feb 12 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.98-1
+ Revision: 637364
- new upstream version 9.0.597.98
- add conflicts to beta channel browser
- add obsoletes entry for old (canary) chromium-browser package

* Thu Feb 10 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.94-1
+ Revision: 637082
- imported package chromium-browser-stable

