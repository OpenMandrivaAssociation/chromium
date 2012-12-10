Summary:	Fast paced, arcade-style, top-scrolling space shooter
Name:		chromium
Version:	0.9.15
Release:	%mkrel 2
License:	Artistic
Group:		Games/Arcade
Source0:	http://downloads.sourceforge.net/%{name}-bsu/%{name}-bsu-%{version}.tar.gz
Patch0:		chromium-0.9.13.3-fix-str-fmt.patch
URL:		http://sourceforge.net/projects/%{name}-bsu
BuildRequires:	quesoglc-devel
BuildRequires:	mesaglu-devel
BuildRequires:	SDL-devel
Buildrequires:	SDL_image-devel
BuildRequires:	openal-devel
BuildRequires:	freealut-devel
BuildRequires:	libglpng-devel
BuildRequires:	imagemagick
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
You are captain of the cargo ship Chromium B.S.U., responsible for delivering
supplies to our troops on the front line. Your ship has a small fleet of
robotic fighters which you control from the relative safety of the Chromium
vessel.
This is an OpenGL-based shoot 'em up game with fine graphics.

%prep
%setup -q -n %{name}-bsu-%{version}
%patch0 -p0

%build
%configure2_5x --bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
%make

%install
rm -fr %buildroot
%makeinstall_std

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m0644 misc/chromium-bsu.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
convert -scale 48x48 misc/chromium-bsu.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32x32 misc/chromium-bsu.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16x16 misc/chromium-bsu.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

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

%find_lang %{name}-bsu

%clean
rm -rf %{buildroot}

%files -f %{name}-bsu.lang
%defattr(-, root, root)
%doc AUTHORS README COPYING NEWS
%{_gamesbindir}/chromium-bsu
%{_gamesdatadir}/*
%{_datadir}/pixmaps/%{name}-bsu.png
%{_datadir}/applications/%{name}-bsu.desktop
%{_docdir}/%{name}-bsu/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man6/*.6*


%changelog
* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 0.9.15-2mdv2011.0
+ Revision: 640428
- rebuild to obsolete old packages

* Tue Feb 15 2011 Zombie Ryushu <ryushu@mandriva.org> 0.9.15-1
+ Revision: 637844
- Upgrade to 0.9.15

* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 0.9.14.1-2
+ Revision: 635015
- rebuild
- tighten BR

* Sun Jul 11 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.9.14.1-1mdv2011.0
+ Revision: 551155
- update to 0.9.14.1, should fix mdv bug#57293
- drop patch1, merged upstream
- fix file list

* Fri May 14 2010 Colin Guthrie <cguthrie@mandriva.org> 0.9.14-2mdv2010.1
+ Revision: 544735
- Fix build error with openal.

* Tue Jul 28 2009 Emmanuel Andry <eandry@mandriva.org> 0.9.14-1mdv2010.0
+ Revision: 402741
- New version 0.9.14
- BR quesoglc-devel
- update files list

* Wed May 20 2009 Funda Wang <fwang@mandriva.org> 0.9.13.3-2mdv2010.0
+ Revision: 377896
- fix str fmt

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Dec 09 2008 Adam Williamson <awilliamson@mandriva.org> 0.9.13.3-1mdv2009.1
+ Revision: 312119
- update URL
- br ftgl-devel
- rebuild
- clean doc file list
- use icon in upstream sources, don't ship it as a set of sources
- drop manual menu entry creation (upstream does it now)
- drop all messy workarounds for old buildsystem as it now properly uses
  autotools
- drop stuff for the setup package
- buildrequires imagemagick (for icons)
- buildrequires libglpng
- setup GUI doesn't exist any more, so don't buildrequire qt3-devel
- drop *all* patches (all merged or superseded upstream)
- update URLs
- new release 0.9.13.3
- clean spec:
  	+ tabs not spaces
  	+ drop unnecessary defines
  	+ use macros not $RPM_*

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Jan 08 2008 Thierry Vignaud <tv@mandriva.org> 0.9.12-29mdv2008.1
+ Revision: 146716
- fix mesaglu-devel BR
- kill re-definition of %%buildroot on Pixel's request
- buildrequires X11-devel instead of XFree86-devel

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Adam Williamson <awilliamson@mandriva.org>
    - add a comment on the debian patches

* Fri Sep 14 2007 Adam Williamson <awilliamson@mandriva.org> 0.9.12-29mdv2008.0
+ Revision: 85458
- disable build of setup tool for now (debian hasn't ported it to new OpenAL API and I don't know how)
- no need to export OPENAL_CONFIG_OPTS
- correct DPKGDATADIR and remove includes parameters for internal OpenAL
- buildrequires openal-devel and freealut-devel
- adopt patches 100-106 from Debian: fix several bugs, port to current OpenAL API, adapt build to use external OpenAL and freealut
- rebuild for 2008
- fd.o icons
- drop X-Mandriva categories
- drop old menu entries

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Sat Dec 02 2006 Olivier Blin <oblin@mandriva.com> 0.9.12-28mdv2007.0
+ Revision: 89978
- XDG menu

* Fri Nov 17 2006 Olivier Blin <oblin@mandriva.com> 0.9.12-27mdv2007.1
+ Revision: 85151
- use system libpng not to be affected by libpng 1.0.2 bugs

* Wed Nov 15 2006 Olivier Blin <oblin@mandriva.com> 0.9.12-26mdv2007.1
+ Revision: 84537
- new release
- link with pthread
- fix icons installation
- bunzip2 sources
- Import chromium

* Sat May 13 2006 Stefan van der Eijk <stefan@eijk.nu> 0.9.12-25mdk
- rebuild for sparc

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.9.12-24mdk
- Rebuild

* Tue Aug 17 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.9.12-23mdk
- Rebuild with new menu

* Sat Jun 05 2004 <lmontel@n2.mandrakesoft.com> 0.9.12-22mdk
- Rebuild

