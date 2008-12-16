#
# Conditional build:
%bcond_without	gtk	# without gtk support
%bcond_without	qt	# without qt support
%bcond_without	gadgets	# without gadgets

# use this to get latest rev:
# svn export http://google-gadgets-for-linux.googlecode.com/svn/trunk/ google-gadgets-for-linux
# TODO:
# - smjs - spidermonkey js runtime (default) is broken with cmake build. revert or fix cmake build!
#   besides, qtjs seems not broken, at least for google calendar widget
# - add gtk BRs
Summary:	google-gadgets-for-linux
Name:		google-gadgets-for-linux
Version:	0.10.4
Release:	1.1
License:	Apache License v2.0
Group:		X11/Applications
Source0:	http://google-gadgets-for-linux.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	0ef0a62e0a575388084a77759b646718
Source1:	%{name}-gtk.desktop
Source2:	%{name}-qt.desktop
Patch0:		%{name}-cmake.patch
Patch1:		%{name}-link_with_qtnetwork.patch
Patch2:		%{name}-js.patch
URL:		http://code.google.com/p/google-gadgets-for-linux/
%if %{with qt}
BuildRequires:	QtCore-devel >= 4.4.3
BuildRequires:	QtNetwork-devel >= 4.4.3
BuildRequires:	QtScript-devel >= 4.4.3
BuildRequires:	QtWebKit-devel >= 4.4.3
%endif
BuildRequires:	cmake >= 2.6.1-2
BuildRequires:	curl-devel >= 7.18.2
BuildRequires:	dbus-devel >= 1.0.2
BuildRequires:	flex
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:	libltdl-devel
BuildRequires:	librsvg-devel
BuildRequires:	libtool >= 1.5.22
BuildRequires:	libxml2-devel >= 2.4.0
BuildRequires:	pkgconfig
BuildRequires:	xulrunner-devel >= 1.8
BuildRequires:	zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Google Gadgets for Linux provides a platform for running desktop
gadgets under Linux, catering to the unique needs of Linux users. It's
compatible with the gadgets written for Google Desktop for Windows as
well as the Universal Gadgets on iGoogle.

%package gadgets
Summary:	google-gadgets set
Summary(pl.UTF-8):	Zestaw gadżetów google-gadgets
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gadgets
Google-gadgets set.

%description gadgets -l pl.UTF-8
Zestaw gadżetów google-gadgets.

%package devel
Summary:	Header files for google-gadgets library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki google-gadgets
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development files assoicated with
libggadget, it is needed to write programs that utilise libggadget.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki google-gadgets.

%package qt
Summary:	Qt Runtime Environment
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description qt
This package contains the QT Google Gadgets library, it is required to
run the QT version of Google Gadgets.

%package gtk
Summary:	GTK Runtime Environment
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
This package contains the GTK+ Google Gadgets library, it is required
to run the GTK+ version of Google Gadgets.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DGTKMOZEMBED_CFLAGS="-I$EMBED_INCDIR/js -I$EMBED_INCDIR/string" \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# desync with cmake/ac makefiles
mv $RPM_BUILD_ROOT%{_datadir}/mime/packages/{00-,}google-gadgets.xml
# desktop files
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/ggl-gtk.desktop
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/ggl-qt.desktop

rm -f $RPM_BUILD_ROOT%{_libdir}/google-gadgets/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libggadget-1.0.so.0
%attr(755,root,root) %{_libdir}/libggadget-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libggadget-dbus-1.0.so.0
%attr(755,root,root) %{_libdir}/libggadget-dbus-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libggadget-js-1.0.so.0
%attr(755,root,root) %{_libdir}/libggadget-js-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libggadget-npapi-1.0.so.0
%attr(755,root,root) %{_libdir}/libggadget-npapi-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libggadget-xdg-1.0.so.0
%attr(755,root,root) %{_libdir}/libggadget-xdg-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/google-gadgets/gtkmoz-browser-child
%dir %{_libdir}/google-gadgets
%dir %{_libdir}/google-gadgets/modules
%dir %{_datadir}/google-gadgets
%{_datadir}/google-gadgets/*.gg
%{_datadir}/mime/packages/google-gadgets.xml
%{_desktopdir}/ggl-designer.desktop
%{_iconsdir}/*/*/*/*.png
%{_pixmapsdir}/google-gadgets.png

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ggl-qt
%attr(755,root,root) %ghost %{_libdir}/libggadget-qt-1.0.so.0
%attr(755,root,root) %{_libdir}/libggadget-qt-1.0.so.*.*.*
%{_libdir}/google-gadgets/modules/qt-edit-element.so
%{_libdir}/google-gadgets/modules/qt-script-runtime.so
%{_libdir}/google-gadgets/modules/qt-system-framework.so
%{_libdir}/google-gadgets/modules/qt-xml-http-request.so
%{_libdir}/google-gadgets/modules/qtwebkit-browser-element.so
%{_desktopdir}/ggl-qt.desktop

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ggl-gtk
%attr(755,root,root) %ghost %{_libdir}/libggadget-gtk-1.0.so.0
%attr(755,root,root) %{_libdir}/libggadget-gtk-1.0.so.*.*.*
%{_libdir}/google-gadgets/modules/gtk-edit-element.so
%{_libdir}/google-gadgets/modules/gtk-flash-element.so
%{_libdir}/google-gadgets/modules/gtk-system-framework.so
%{_desktopdir}/ggl-gtk.desktop

%files gadgets
%defattr(644,root,root,755)
%{_libdir}/google-gadgets/modules/analytics-usage-collector.so
%{_libdir}/google-gadgets/modules/curl-xml-http-request.so
%{_libdir}/google-gadgets/modules/dbus-script-class.so
%{_libdir}/google-gadgets/modules/default-framework.so
%{_libdir}/google-gadgets/modules/default-options.so
%{_libdir}/google-gadgets/modules/google-gadget-manager.so
%{_libdir}/google-gadgets/modules/gst-audio-framework.so
%{_libdir}/google-gadgets/modules/gst-video-element.so
%{_libdir}/google-gadgets/modules/gtkmoz-browser-element.so
%{_libdir}/google-gadgets/modules/libxml2-xml-parser.so
%{_libdir}/google-gadgets/modules/linux-system-framework.so
%{_libdir}/google-gadgets/modules/smjs-script-runtime.so

%files devel
%defattr(644,root,root,755)
%dir %{_libdir}/google-gadgets/include
%dir %{_libdir}/google-gadgets/include/ggadget
%{_libdir}/google-gadgets/include/ggadget/*.h
%dir %{_includedir}/google-gadgets
%dir %{_includedir}/google-gadgets/ggadget
%{_includedir}/google-gadgets/ggadget/*.h
%dir %{_includedir}/google-gadgets/ggadget/dbus
%{_includedir}/google-gadgets/ggadget/dbus/*.h
%dir %{_includedir}/google-gadgets/ggadget/gtk
%{_includedir}/google-gadgets/ggadget/gtk/*.h
%dir %{_includedir}/google-gadgets/ggadget/npapi
%{_includedir}/google-gadgets/ggadget/npapi/*.h
%dir %{_includedir}/google-gadgets/ggadget/qt
%{_includedir}/google-gadgets/ggadget/qt/*.h
%dir %{_includedir}/google-gadgets/ggadget/js
%{_includedir}/google-gadgets/ggadget/js/*.h
%dir %{_includedir}/google-gadgets/ggadget/xdg
%{_includedir}/google-gadgets/ggadget/xdg/*.h
%attr(755,root,root) %{_libdir}/*.so
%{_pkgconfigdir}/*.pc
