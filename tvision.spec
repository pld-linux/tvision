Summary:	Unix port of Borland TurboVision library
Summary(pl):	Unixowa wersja biblioteki TurboVision Borlanda
Name:		tvision
Version:	0.7
Release:	3
Copyright:	Borland, some modifications are BSD-style licensed (generally free)
Group:		Libraries
Group(pl):	Biblioteki
Source:		%{name}-%{version}.tar.gz
Patch:		%{name}-info.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Turbo Vision (or TV, for short) is a library that provides an application
framework.  With TV you can write a beautiful object-oriented character-mode
user interface in a short time.

TV is available in C++ and Pascal and is a product of Borland International.
It was developed to run on MS-DOS systems, but today it is available for many
other platforms (ported by independent programmers).

This port is based on the Borland 2.0 version with fixes.

%description -l pl
Unixowa wersja biblioteki TurboVision Borlanda

%package devel
Summary:	%{name} header files
Summary(pl):	Pliki nag³ówkowe %{name}
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
%{name} header files.

%description -l pl devel
Pliki nag³ówkowe %{name}.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static %{name} libraries.

%description -l pl static
Biblioteki statyczne %{name}.


%prep
%setup -q
%patch -p1

%build
CPPFLAGS="-I%{_includedir}/ncurses/"; export CPPFLAGS
%configure

sed 's|<sys/time.h>|<time.h>|' demo/puzzle.cc > demo/puzzle.cc.$$ && mv -f demo/puzzle.cc.$$ demo/puzzle.cc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_infodir}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/{demo,tutorial}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install doc/tvision.info $RPM_BUILD_ROOT%{_infodir}

# some cleaning
%{__make} -C tutorial mostlyclean
%{__make} -C demo     mostlyclean
rm demo/Makefile*
rm tutorial/Makefile*
rm doc/{*.info,*.texi,*.tex,*.sed,*.kdoc,Makefile*}

mv demo/demo			$RPM_BUILD_ROOT%{_libdir}/%{name}/demo
mv tutorial/tvguid[0-9][0-9]	$RPM_BUILD_ROOT%{_libdir}/%{name}/tutorial

# let's create simple Makefile ("\$" to prevent from macro expansion)
cat >tutorial/Makefile  <<EOF
CPPFLAGS = -g
LDFLAGS = -lncurses -lgpm -ltvision

SOURCES := \$(wildcard *.cc)
PROGS   := \$(patsubst %.cc,%,\$(SOURCES))

all: \$(PROGS)
EOF

gzip -9nf ChangeLog README TODO Announce COPYRIGHT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%fix_info_dir

%postun
/sbin/ldconfig
%fix_info_dir

%files
%defattr(644,root,root,755)
%doc doc demo tutorial ChangeLog.gz README.gz TODO.gz Announce.gz COPYRIGHT.gz
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/%{name}
%{_infodir}/*


%files devel
%{_includedir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%attr(644,root,root) %{_libdir}/lib*.a
