Summary:	Fast paced, arcade-style, top-scrolling space shooter
Name:		chromium
Version:	0.9.13.3
Release:	%{mkrel 1}
License:	Artistic
Group:		Games/Arcade
Source0:	http://downloads.sourceforge.net/%{name}-bsu/%{name}-%{version}.tar.gz
URL:		http://sourceforge.net/projects/%{name}-bsu
BuildRequires:	SDL-devel
BuildRequires:	X11-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	esound-devel
BuildRequires:	mesaglu-devel
BuildRequires:	libogg-devel
BuildRequires:	libsmpeg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	texinfo
BuildRequires:	png-devel
BuildRequires:	zlib-devel
BuildRequires:	openal-devel
BuildRequires:	freealut-devel
BuildRequires:	libglpng-devel
BuildRequires:	ftgl-devel
BuildRequires:	ImageMagick
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
You are captain of the cargo ship Chromium B.S.U., responsible for delivering
supplies to our troops on the front line. Your ship has a small fleet of
robotic fighters which you control from the relative safety of the Chromium
vessel.
This is an OpenGL-based shoot 'em up game with fine graphics.

%prep
%setup -q

%build
%configure2_5x --bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
%make

%install
%makeinstall_std

#install -d %{buildroot}%{_datadir}/applications
#cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
#[Desktop Entry]
#Name=Chromium
#Comment=Shoot 'em up game
#Exec=soundwrapper %{_gamesbindir}/%{name}
#Icon=%{name}
#Terminal=false
#Type=Application
#Categories=Game;ArcadeGame;
#EOF

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m0644 misc/chromium.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
convert -scale 48x48 misc/chromium.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32x32 misc/chromium.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16x16 misc/chromium.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

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

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS README COPYING NEWS TODO
%{_gamesbindir}/chromium
%{_gamesdatadir}/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man6/*.6*

