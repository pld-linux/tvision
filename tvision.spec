Summary:	Unix port of Borland TurboVision library
Summary(pl):	Unixowa wersja biblioteki TurboVision Borlanda
Name:		tvision
Version:	0.7
Release:	2
Copyright:	Borland, some modifications are BSD-style licensed
Group:		Libraries
Group(pl):	Biblioteki
Source:		%{name}-%{version}.tar.gz
BuildRoot:	/tmp/%{name}-%{version}-root

%description

%prep
%setup -q

%build
CPPFLAGS="$RPM_OPT_FLAGS -I/usr/include/ncurses/"; export CPPFLAGS
LDFLAGS="-s"; export LDFLAGS
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_includedir},%{_infodir}}
make install DESTDIR=$RPM_BUILD_ROOT

install doc/tvision.info $RPM_BUILD_ROOT%{_infodir}

# some cleaning
make -C tutorial mostlyclean
make -C demo     mostlyclean
rm doc/{*.info,*.texi,*.tex,*.sed,*.kdoc,Makefile*}

cp -a demo     $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a tutorial $RPM_BUILD_ROOT%{_libdir}/%{name}

gzip -9nf ChangeLog README TODO Announce COPYRIGHT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1 

%postun
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1 

%files
%defattr(644,root,root,755)
%doc doc demo tutorial ChangeLog.gz README.gz TODO.gz Announce.gz COPYRIGHT.gz
# !!!! .a file to be separated %{_libdir}/lib%{name}.so*
%{_libdir}/lib%{name}.*
%{_includedir}/*
%{_infodir}/*
%attr(755,root,root) %{_libdir}/%{name}/tutorial/tvguid[0-9][0-9]
%{_libdir}/%{name}/tutorial/tvguid[0-9][0-9].*
%{_libdir}/%{name}/tutorial/Makefile*

%attr(755,root,root) %{_libdir}/%{name}/demo/demo
%{_libdir}/%{name}/demo/*.{cc,h}
%{_libdir}/%{name}/demo/Makefile*
