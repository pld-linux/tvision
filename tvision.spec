Summary:	Unix port of Borland TurboVision library
Summary(pl):	Uniksowa wersja biblioteki TurboVision Borlanda
Name:		tvision
Version:	0.8
Release:	3
License:	Borland, some modifications are BSD-like licensed (generally free)
Group:		Libraries
Source0:	ftp://sunsite.unc.edu/pub/Linux/devel/lang/c++/%{name}-%{version}.tar.gz
Patch0:		%{name}-info.patch
Patch1:		%{name}-am_fixes.patch
Patch2:		%{name}-endian.h.patch
BuildRequires:	gcc-c++
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
Prereq:		/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Turbo Vision (or TV, for short) is a library that provides an
application framework. With TV you can write a beautiful
object-oriented character-mode user interface in a short time.

TV is available in C++ and Pascal and is a product of Borland
International. It was developed to run on MS-DOS systems, but today it
is available for many other platforms (ported by independent
programmers).

This port is based on the Borland 2.0 version with fixes.

%description -l pl
Uniksowa wersja biblioteki TurboVision 2.0 Borlanda. TurboVision jest
obiektow± bibliotek± do okienkowych interfejsów u¿ytkownika w trybie
tekstowym.

%package devel
Summary:	%{name} header files
Summary(pl):	Pliki nag³ówkowe %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
tvision header files.

%description devel -l pl
Pliki nag³ówkowe tvision.

%package static
Summary:	Static %{name} libraries
Summary(pl):	Biblioteki statyczne %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static tvision libraries.

%description static -l pl
Biblioteki statyczne tvision.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CXXFLAGS="-I%{_includedir}/ncurses -fno-exceptions -fno-rtti -fno-implicit-templates"
%configure

sed 's|<sys/time.h>|<time.h>|' demo/puzzle.cc > demo/puzzle.cc.$$ && mv -f demo/puzzle.cc.$$ demo/puzzle.cc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_examplesdir}/%{name}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install doc/tvision.info $RPM_BUILD_ROOT%{_infodir}

# some cleaning
%{__make} -C tutorial mostlyclean
%{__make} -C demo     mostlyclean
rm -f demo/Makefile*
rm -f tutorial/Makefile*
rm -f doc/{*.info,*.texi,*.tex,*.sed,*.kdoc,Makefile*}

# let's create simple Makefile ("\$" to prevent from macro expansion)
cat >tutorial/Makefile  <<EOF
CPPFLAGS = -g
LDFLAGS = -lncurses -lgpm -ltvision

SOURCES := \$(wildcard *.cc)
PROGS   := \$(patsubst %.cc,%,\$(SOURCES))

all: \$(PROGS)
EOF

cp -ar demo tutorial $RPM_BUILD_ROOT%{_examplesdir}/%{name}

gzip -9nf ChangeLog README TODO Announce COPYRIGHT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc doc *.gz
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_infodir}/*

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_includedir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_examplesdir}/%{name}

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
