#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	gui		# mixer utility
#
Summary:	Free FireWire audio driver library
Summary(pl.UTF-8):	Wolnodostępna biblioteka sterownika dźwięku FireWire
Name:		libffado
Version:	2.0.0
Release:	2
License:	GPL v2 or GPL v3
Group:		Libraries
#Source0Download: http://www.ffado.org/?q=node/5
Source0:	http://www.ffado.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	89fd874731a1437043d0a57ed87c81ef
Patch0:		%{name}-gcc4.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-api-doc-only.patch
URL:		http://www.ffado.org/
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	jack-audio-connection-kit-devel >= 0.109.12
BuildRequires:	libiec61883-devel >= 1.1.0
BuildRequires:	libraw1394-devel >= 1.3.0
BuildRequires:	libstdc++-devel
BuildRequires:	libxml++-devel >= 2.6.13
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
BuildRequires:	python-dbus-devel >= 0.82.0
%endif
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
Requires(post,postun):  desktop-file-utils
Requires:	%{name} = %{version}-%{release}
Requires:       gtk-update-icon-cache
Requires:       hicolor-icon-theme
Requires:	python-PyQt4 >= 4
Requires:	python-dbus >= 0.82.0

%description gui
Graphical mixer utility for FFADO.

%description gui -l pl.UTF-8
Graficzny mikser dla FFADO.

%prep
%setup -q
%patch0 -p2
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%{rpmcflags} -fPIC"
export CCFLAGS="%{rpmcxxflags} -fPIC"
export LDFLAGS="%{rpmldflags}"
%{__scons} \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}


%if %{with apidocs}
%{__scons} doc
%{__make} -C doc/reference/latex
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_iconsdir}/hicolor/64x64/apps}

# scons sucks
export CFLAGS="%{rpmcflags}"
export CCFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"

%{__scons} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with gui}
# scons sucks even more
desktop-file-install --dir $RPM_BUILD_ROOT%{_desktopdir} support/xdg/ffado.org-ffadomixer.desktop
ln -s ../../../../libffado/icons/hi64-apps-ffado.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/64x64/apps/ffado.png
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
%attr(755,root,root) %{_bindir}/ffado-bridgeco-downloader
%attr(755,root,root) %{_bindir}/ffado-dbus-server
%attr(755,root,root) %{_bindir}/ffado-fireworks-downloader
%attr(755,root,root) %{_bindir}/ffado-test
%attr(755,root,root) %{_bindir}/ffado-test-isorecv
%attr(755,root,root) %{_bindir}/ffado-test-isoxmit
%attr(755,root,root) %{_bindir}/ffado-test-streaming
%attr(755,root,root) %{_libdir}/libffado.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libffado.so.2
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/configuration
%dir %{_datadir}/%{name}/python

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libffado.so
%{_includedir}/libffado
%{_pkgconfigdir}/libffado.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/reference/html doc/reference/latex/*.pdf
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
%{_datadir}/%{name}/python/ffado_configuration.py
%{_datadir}/%{name}/python/ffado_dbus_util.py
%{_datadir}/%{name}/python/ffado_panelmanager.py
%{_datadir}/%{name}/python/ffado_panelmanagerstatusui.py
%{_datadir}/%{name}/python/ffado_regdialog.py
%{_datadir}/%{name}/python/ffado_regdialogui.py
%{_datadir}/%{name}/python/ffado_registration.py
%{_datadir}/%{name}/python/ffadomixer_config.py
%{_datadir}/%{name}/python/mixer_*.py
%{_desktopdir}/ffado.org-ffadomixer.desktop
%{_iconsdir}/hicolor/*/apps/ffado.png
%endif
