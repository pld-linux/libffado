#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	gui		# mixer utility
%bcond_with	jack1		# use JACK 1 (0.12x) instead of JACK 2 (1.9.x)

Summary:	Free FireWire audio driver library
Summary(pl.UTF-8):	Wolnodostępna biblioteka sterownika dźwięku FireWire
Name:		libffado
Version:	2.4.9
Release:	1
License:	GPL v2 or GPL v3
Group:		Libraries
#Source0Download: https://ffado.org/?q=node/5
Source0:	https://ffado.org/files/%{name}-%{version}.tgz
# Source0-md5:	8e20b9d52a42707cc03f91fa5996b027
Patch1:		detect-x32.patch
URL:		https://ffado.org/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	dbus-c++-devel
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	doxygen
%if %{with jack1}
BuildRequires:	jack-audio-connection-kit-devel < 1.9.0
BuildRequires:	jack-audio-connection-kit-devel >= 0.122.0
%else
BuildRequires:	jack-audio-connection-kit-devel >= 1.9.9
%endif
BuildRequires:	libavc1394-devel >= 0.5.3
BuildRequires:	libconfig-c++-devel
BuildRequires:	libiec61883-devel >= 1.1.0
BuildRequires:	libraw1394-devel >= 2.0.5
# -std=gnu++11 for libxml++ 2.40+
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libxml++-devel >= 3.0.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	scons >= 4
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
BuildRequires:	python-dbus-devel >= 0.82.0
BuildRequires:	python3-PyQt5-devel-tools >= 5
BuildRequires:	python3-PyQt5-uic >= 5
%endif
Requires:	libavc1394 >= 0.5.3
Requires:	libiec61883 >= 1.1.0
Requires:	libraw1394 >= 2.0.5
Requires:	libxml++ >= 3.0.0
Suggests:	qjackctl >= 0.2.20.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The FFADO project aims to provide a generic, open-source solution for
the support of FireWire based audio devices for the Linux platform. It
is the successor of the FreeBoB project.

%description -l pl.UTF-8
Celem projektu FFADO jest dostarczenie ogólnego, mającego otwarte
źródła rozwiązania do obsługi urządzeń dźwiękowych FireWire pod
Linuksem. Projekt jest następcą projektu FireBoB.

%package devel
Summary:	Header files for FFADO library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FFADO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libffado-static < 2.0.0

%description devel
Header files for FFADO library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FFADO.

%package apidocs
Summary:	FFADO API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki FFADO
Group:		Documentation
BuildArch:	noarch

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
Requires:	python3-PyQt5 >= 5
Requires:	python3-dbus >= 0.82.0

%description gui
Graphical mixer utility for FFADO.

%description gui -l pl.UTF-8
Graficzny mikser dla FFADO.

%prep
%setup -q
%patch1 -p1

# force python3
%{__sed} -i -e '1s,/usr/bin/python$,%{__python3},' \
	admin/*.py \
	support/mixer-qt4/ffado-mixer-profiler.in

%build
%{__scons} \
	COMPILE_FLAGS="%{rpmcxxflags}" \
	ENABLE_ALL=True \
	PREFIX=%{_prefix} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir} \
	PYPKGDIR=%{py3_sitescriptdir} \
	PYTHON_INTERPRETER=%{__python3}

%if %{with apidocs}
%{__scons} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_iconsdir}/hicolor/64x64/apps}

%{__scons} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/test-*

%if %{with gui}
## scons sucks
#desktop-file-install --dir $RPM_BUILD_ROOT%{_desktopdir} support/xdg/ffado.org-ffadomixer.desktop
#ln -s ../../../../libffado/icons/hi64-apps-ffado.png \
#	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/64x64/apps/ffado.png

%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
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
%doc doc/reference/html
%endif

%files diag
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ffado-diag
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/static_info.txt

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ffado-mixer
%{_datadir}/%{name}/icons
%{py3_sitescriptdir}/ffado
%{_datadir}/metainfo/org.ffado.FfadoMixer.metainfo.xml
%{_desktopdir}/org.ffado.FfadoMixer.desktop
%{_iconsdir}/hicolor/64x64/apps/hi64-apps-ffado.png
%{_mandir}/man1/ffado-mixer.1*
%endif
