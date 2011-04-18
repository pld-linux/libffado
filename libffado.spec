#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_with	static_libs	# don't build static libraries
#
Summary:	Free firewire audio driver library
#Summary(pl.UTF-8):	-
Name:		libffado
Version:	2.0.0
Release:	0.1
License:	GPLv2/GPLv3
Group:		Libraries
Source0:	http://www.ffado.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	89fd874731a1437043d0a57ed87c81ef
Patch0:		%{name}-gcc4.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-api-doc-only.patch
URL:		http://www.ffado.org/
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libiec61883-devel >= 1.1.0
BuildRequires:	libraw1394-devel
BuildRequires:	libxml++-devel
BuildRequires:	python-dbus-devel
BuildRequires:	python-PyQt4-devel
BuildRequires:	scons
BuildRequires:	texlive-format-pdflatex
Requires(post,postun):  desktop-file-utils
Requires:       gtk-update-icon-cache
Requires:       hicolor-icon-theme
Suggests:	qjackctl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The FFADO project aims to provide a generic, open-source solution for
the support of FireWire based audio devices for the Linux platform.
It is the successor of the FreeBoB project.

#%description -l pl.UTF-8

%package devel
Summary:	Header files for FFADO library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FFADO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for FFADO library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FFADO.

%package static
Summary:	Static FFADO library
Summary(pl.UTF-8):	Statyczna biblioteka FFADO
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FFADO library.

%description static -l pl.UTF-8
Statyczna biblioteka FFADO.

%package apidocs
Summary:	FFADO API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki FFADO
Group:		Documentation

%description apidocs
API and internal documentation for FFADO library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki FFADO.

%prep
%setup -q
%patch0 -p2
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%{rpmcflags} -fPIC"
export CCFLAGS="%{rpmcxxflags} -fPIC"
export LDFLAGS="%{rpmldflags}"
export BUILD_STATIC_LIB=%{?with_static_libs:yes}%{!?with_static_libs:no}
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
export BUILD_STATIC_LIB=%{?with_static_libs:yes}%{!?with_static_libs:no}

%{__scons} install \
	DESTDIR=$RPM_BUILD_ROOT

# scons sucks even more
desktop-file-install --dir $RPM_BUILD_ROOT%{_desktopdir} support/xdg/ffado.org-ffadomixer.desktop
ln -s ../../../../libffado/icons/hi64-apps-ffado.png \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/64x64/apps/ffado.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %ghost %{_libdir}/libffado.so.2
%attr(755,root,root) %{_libdir}/libffado.so.*.*.*
%{_datadir}/%{name}
%{_desktopdir}/ffado.org-ffadomixer.desktop
%{_iconsdir}/hicolor/*/apps/ffado.png

%files devel
%defattr(644,root,root,755)
%{_libdir}/libffado.so
%{_includedir}/libffado
%{_pkgconfigdir}/libffado.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libffado.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/reference/html doc/reference/latex/*.pdf
%endif
