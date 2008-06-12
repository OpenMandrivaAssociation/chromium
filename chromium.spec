%define name chromium
%define version 0.9.12
%define release %mkrel 29

Summary: Fast paced, arcade-style, top-scrolling space shooter
Name: %{name}
Version: %{version}
Release: %{release}
License: Artistic
Group: Games/Arcade
Source: http://www.reptilelabour.com/software/files/chromium/chromium-src-%{version}.tar.bz2
Source1: http://www.reptilelabour.com/software/files/chromium/chromium-data-%{version}.tar.bz2
Source10: %{name}.16.png
Source11: %{name}.32.png
Source12: %{name}.48.png
URL: http://www.reptilelabour.com/software/chromium/
Patch0: chromium-0.9.12-fix-flags.patch
Patch1: chromium-0.9.11-glibc-2.2.2.patch
Patch3: chromium-fix-gcc-2.96.patch
Patch5: chromium-0.9.12-fix-openal-configurecall.patch
Patch6: chromium-0.9.12-shared-zlib.patch
Patch7: chromium-0.9.12-fix-gcc31.patch
Patch8: chromium-0.9.12-fix-qt3.patch
Patch9: chromium-0.9.12-pthread.patch
Patch10: chromium-0.9.12-system-png.patch

# Debian patches. 10_buildfixes.dpatch is modified from the Debian
# version in several ways - some changes that are Debian-specific are
# left out, and in our version, internal libglpng is still used
# (Debian uses a system copy, but we don't have one). Other patches
# are unmodified from the Debian versions. - AdamW 2007/09
Patch100: 10_buildfixes.dpatch
Patch101: 15_soundfix.dpatch
Patch102: 20_badcode.dpatch
Patch103: 25_gcc4.dpatch
Patch104: 30_new_openAL.dpatch
Patch105: 35_powerup_crash.diff
Patch106: 40_sdl_quit.diff

BuildRequires:	SDL-devel
BuildRequires:	X11-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	esound-devel
BuildRequires:	mesaglu-devel
BuildRequires:	libogg-devel
BuildRequires:	libsmpeg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	qt3-devel
BuildRequires:	texinfo
BuildRequires:	png-devel
BuildRequires:	zlib-devel
BuildRequires:	openal-devel
BuildRequires:	freealut-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
You are captain of the cargo ship Chromium B.S.U., responsible for delivering
supplies to our troops on the front line. Your ship has a small fleet of
robotic fighters which you control from the relative safety of the Chromium
vessel.
This is an OpenGL-based shoot 'em up game with fine graphics.

%package setup
Summary: Setup frontend for Chromium
Group: Games/Arcade
Requires: %{name} = %{version}-%{release}

%description setup
This package contains the setup frontend (using QT) to ease configuration
of Chromium, especially for its playlist features.

%prep
%setup -q -n Chromium-0.9
%patch0 -p0
%patch1 -p0
%patch3 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p0
%patch10 -p1 -b .png
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1

# Nuke references to -L/usr/lib and -L/usr/local/lib
find . -name Makefile | xargs \
  perl -pi -e "s,-L/usr(/local)?/lib\b,,g"

# Make it lib64 aware
find . -name Makefile -or -name configure | xargs \
  perl -pi -e "s,(/usr(/X11R6)?|\\\$\(QTDIR\))/lib\b,\1/%{_lib},g"

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer"
export DEFS="-DGAMESBINDIR=\\\"%{_gamesbindir}\\\" -DPKGDATADIR=\\\"%{_gamesdatadir}/Chromium-0.9/data\\\" -DUSE_SDL `sdl-config --cflags` -DAUDIO_OPENAL -D_REENTRANT -I../../include"
# QTDIR will alway be in /usr/lib whatever the platform may it be
export QTDIR=%{_prefix}/lib/qt3
./configure --enable-vorbis --disable-setup
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_gamesbindir}
cp bin/* $RPM_BUILD_ROOT/%{_gamesbindir}
mkdir -p $RPM_BUILD_ROOT/%{_gamesdatadir}
tar jxvf %{SOURCE1} -C $RPM_BUILD_ROOT/%{_gamesdatadir}

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Chromium
Comment=Shoot 'em up game
Exec=soundwrapper %{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

#cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-setup.desktop << EOF
#[Desktop Entry]
#Name=Chromium setup
#Comment=Graphical setup tool for Chromium
#Exec=%{_gamesbindir}/%{name}-setup
#Icon=%{name}
#Terminal=false
#Type=Application
#Categories=Game;ArcadeGame;
#EOF

mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

install %{SOURCE10} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install %{SOURCE11} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install %{SOURCE12} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png

rm -rf `find $RPM_BUILD_ROOT -type d -name .xvpics`

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%post setup
%{update_menus}
%endif

%if %mdkversion < 200900
%postun setup
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc README LICENSE CHANGES
%{_gamesbindir}/chromium
%{_gamesdatadir}/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

#%files setup
#%defattr(-, root, root)
#%doc README
#%{_gamesbindir}/chromium-setup
#%{_datadir}/applications/mandriva-%{name}-setup.desktop

