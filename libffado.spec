#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	gui		# mixer utility
%bcond_with	jack1		# use JACK 1 instead of JACK 2-pre
#
Summary:	Free FireWire audio driver library
Summary(pl.UTF-8):	Wolnodostępna biblioteka sterownika dźwięku FireWire
Name:		libffado
Version:	2.2.1
Release:	4
License:	GPL v2 or GPL v3
Group:		Libraries
#Source0Download: http://www.ffado.org/?q=node/5
Source0:	http://www.ffado.org/files/%{name}-%{version}.tgz
# Source0-md5:	e113d828835051f835fb4a329cb0cbd4
Patch0:		%{name}-api-doc-only.patch
Patch1:		detect-x32.patch
Patch2:		%{name}-c++.patch
URL:		http://www.ffado.org/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	dbus-c++-devel
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	doxygen
%if %{with jack1}
BuildRequires:	jack-audio-connection-kit-devel >= 0.122.0
BuildRequires:	jack-audio-connection-kit-devel < 1.9.0
%else
BuildRequires:	jack-audio-connection-kit-devel >= 1.9.9
%endif
BuildRequires:	libavc1394-devel >= 0.5.3
BuildRequires:	libconfig-c++-devel
BuildRequires:	libiec61883-devel >= 1.1.0
BuildRequires:	libraw1394-devel >= 2.0.5
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	libxml++2-devel >= 2.13.0
BuildRequires:	pkgconfig
BuildRequires:	scons
%if %{with apidocs}
BuildRequires:	texlive-fonts-rsfs
BuildRequires:	texlive-format-pdflatex
# for colortbl.sty
BuildRequires:	texlive-latex-extend
BuildRequires:	texlive-makeindex
# for ifxetex.sty needed by some package (texlive packaging error?)
BuildRequires:	texlive-xetex
%endif
%if %{with gui}
BuildRequires:	desktop-file-utils
BuildRequires:	python-PyQt4-devel-tools >= 4
BuildRequires:	python-PyQt4-uic >= 4
BuildRequires:	python-dbus-devel >= 0.82.0
%endif
Requires:	libavc1394 >= 0.5.3
Requires:	libiec61883 >= 1.1.0
Requires:	libraw1394 >= 2.0.5
Requires:	libxml++2 >= 2.13.0
Suggests:	qjackctl >= 0.2.20.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The FFADO project aims to provide a generic, open-source solution for
the support of FireWire based audio devices for the Linux platform.
It is the successor of the FreeBoB project.

%description -l pl.UTF-8
Celem projektu FFADO jest dostarczenie ogólnego, mającego otwarte
źródła rozwiązania do obsługi urządzeń dźwiękowych FireWire pod
Linuksem. Projekt jest następcą projektu FireBoB.

%package devel
Summary:	Header files for FFADO library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FFADO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libffado-static

%description devel
Header files for FFADO library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FFADO.

%package apidocs
Summary:	FFADO API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki FFADO
Group:		Documentation

%description apidocs
API and internal documentation for FFADO library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki FFADO.

%package diag
Summary:	FFADO diagnostic utility
Summary(pl.UTF-8):	Narzędzie diagnostyczne FFADO
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description diag
FFADO diagnostic utility written in Python.

%description diag -l pl.UTF-8
Narzędzie diagnostyczne FFADO napisane w Pythonie.

%package gui
Summary:	Graphical mixer utility
Summary(pl.UTF-8):	Graficzny mikser
Group:		X11/Applications/Sound
Requires(post,postun):	desktop-file-utils
Requires:	%{name} = %{version}-%{release}
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	python-PyQt4 >= 4
Requires:	python-dbus >= 0.82.0

%description gui
Graphical mixer utility for FFADO.

%description gui -l pl.UTF-8
Graficzny mikser dla FFADO.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# libxml++ 2.40+ requires C++ 11
%{__scons} \
	COMPILE_FLAGS="%{rpmcxxflags} -std=gnu++0x" \
	ENABLE_ALL=True \
	PREFIX=%{_prefix} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir} \
	PYPKGDIR=%{py_sitescriptdir}

%if %{with apidocs}
%{__scons} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_iconsdir}/hicolor/64x64/apps}

%{__scons} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/test-*

%if %{with gui}
# scons sucks
desktop-file-install --dir $RPM_BUILD_ROOT%{_desktopdir} support/xdg/ffado.org-ffadomixer.desktop
ln -s ../../../../libffado/icons/hi64-apps-ffado.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/64x64/apps/ffado.png

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post gui
%update_desktop_database_post
%update_icon_cache hicolor

%postun gui
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/dumpiso_mod
%attr(755,root,root) %{_bindir}/ffado-bridgeco-downloader
%attr(755,root,root) %{_bindir}/ffado-dbus-server
%attr(755,root,root) %{_bindir}/ffado-dice-firmware
%attr(755,root,root) %{_bindir}/ffado-fireworks-downloader
%attr(755,root,root) %{_bindir}/ffado-set-nickname
%attr(755,root,root) %{_bindir}/ffado-test
%attr(755,root,root) %{_bindir}/ffado-test-isorecv
%attr(755,root,root) %{_bindir}/ffado-test-isoxmit
%attr(755,root,root) %{_bindir}/ffado-test-streaming
%attr(755,root,root) %{_bindir}/ffado-test-streaming-ipc
%attr(755,root,root) %{_bindir}/ffado-test-streaming-ipcclient
%attr(755,root,root) %{_bindir}/gen-loadpulses
%attr(755,root,root) %{_bindir}/scan-devreg
%attr(755,root,root) %{_bindir}/set-default-router-config-dice-eap
%attr(755,root,root) %{_bindir}/unmute-ozonic
%attr(755,root,root) %{_libdir}/libffado.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libffado.so.2
%dir %{_datadir}/%{name}
%{_datadir}/libffado/fw410.xml
%{_datadir}/libffado/fwap.xml
%{_datadir}/libffado/refdesign.xml
%{_datadir}/%{name}/configuration
%dir %{_datadir}/%{name}/python
%{_mandir}/man1/ffado-bridgeco-downloader.1*
%{_mandir}/man1/ffado-dbus-server.1*
%{_mandir}/man1/ffado-diag.1*
%{_mandir}/man1/ffado-dice-firmware.1*
%{_mandir}/man1/ffado-fireworks-downloader.1*
%{_datadir}/dbus-1/services/org.ffado.Control.service
/lib/udev/rules.d/60-ffado.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libffado.so
%{_includedir}/libffado
%{_pkgconfigdir}/libffado.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/reference/html doc/reference/html/*
%endif

%files diag
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ffado-diag
%{_datadir}/%{name}/python/ffado_diag_helpers.py
%{_datadir}/%{name}/python/helpstrings.py
%{_datadir}/%{name}/python/listirqinfo.py
%{_datadir}/%{name}/python/static_info.txt

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ffado-mixer
%{_datadir}/%{name}/icons
%{py_sitescriptdir}/ffado
%{_desktopdir}/ffado.org-ffadomixer.desktop
%{_iconsdir}/hicolor/*/apps/ffado.png
%{_mandir}/man1/ffado-mixer.1*
%endif
