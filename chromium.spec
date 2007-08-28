%define name chromium
%define version 0.9.12
%define release %mkrel 28

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

BuildRequires:	SDL-devel
BuildRequires:	XFree86-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	esound-devel
BuildRequires:	libMesaGLU-devel
BuildRequires:	libogg-devel
BuildRequires:	libsmpeg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	qt3-devel
BuildRequires:	texinfo
BuildRequires:	png-devel
BuildRequires:	zlib-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
You are captain of the cargo ship Chromium B.S.U., responsible for delivering
supplies to our troops on the front line. Your ship has a small fleet of
robotic fighters which you control from the relative safety of the Chromium
vessel.
This is an OpenGL-based shoot them up game with fine graphics.

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

# Nuke references to -L/usr/lib and -L/usr/local/lib
find . -name Makefile | xargs \
  perl -pi -e "s,-L/usr(/local)?/lib\b,,g"

# Make it lib64 aware
find . -name Makefile -or -name configure | xargs \
  perl -pi -e "s,(/usr(/X11R6)?|\\\$\(QTDIR\))/lib\b,\1/%{_lib},g"

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer"
export DEFS="-DGAMESBINDIR=\\\"%{_gamesbindir}\\\" -DPKGDATADIR=\\\"%{_gamesdatadir}/Chromium-0.9\\\" -DUSE_SDL `sdl-config --cflags` -DOLD_OPENAL -DAUDIO_OPENAL -D_REENTRANT -I../../include -I../support/openal/linux/include -I../support/openal/include"
export OPENAL_CONFIG_OPTS="./configure %{_target_platform}"
# QTDIR will alway be in /usr/lib whatever the platform may it be
export QTDIR=%{_prefix}/lib/qt3
./configure --enable-vorbis
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_gamesbindir}
cp bin/* $RPM_BUILD_ROOT/%{_gamesbindir}
mkdir -p $RPM_BUILD_ROOT/%{_gamesdatadir}
tar jxvf %{SOURCE1} -C $RPM_BUILD_ROOT/%{_gamesdatadir}

mkdir -p $RPM_BUILD_ROOT/%{_menudir}
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/%{name}
?package(%{name}):command="%{_gamesbindir}/%{name}" icon="%{name}.png" \
  needs="x11" section="Amusement/Arcade" title="Chromium" \
  longtitle="OpenGL shoot them up"
EOF

cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/chromium-setup
?package(chromium-setup):command="%{_gamesbindir}/chromium-setup" icon="%{name}.png" \
  needs="x11" section="Amusement/Arcade" title="Chromium Setup" \
  longtitle="Graphical Setup of Chromium"
EOF

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Chromium
Comment=OpenGL shoot them up
Exec=soundwrapper %{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-setup.desktop << EOF
[Desktop Entry]
Name=Chromium Setup
Comment=Graphical Setup of Chromium
Exec=%{_gamesbindir}/%{name}-setup
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
install %{SOURCE10} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install %{SOURCE11} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install %{SOURCE12} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

rm -rf `find $RPM_BUILD_ROOT -type d -name .xvpics`

%post
%{update_menus}

%postun
%{clean_menus}

%post setup
%{update_menus}

%postun setup
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc README LICENSE CHANGES
%{_gamesbindir}/chromium
%{_gamesdatadir}/*
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files setup
%defattr(-, root, root)
%doc README
%{_gamesbindir}/chromium-setup
%{_menudir}/chromium-setup
%{_datadir}/applications/mandriva-%{name}-setup.desktop


