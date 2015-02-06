%define major 4
%define libname %mklibname log4cpp %{major}
%define develname %mklibname log4cpp -d

Summary:	Log for C++
Name:		log4cpp
Version:	1.0
Release:	3
License:	LGPLv2+
Group:		System/Libraries
URL:		http://log4cpp.sourceforge.net/
Source0:	%{name}-%{version}.tar.gz
Patch0:		log4cpp-1.0-gcc43.patch
Patch1:		log4cpp-1.0-remove-pc-cflags.patch
Patch2:		log4cpp-1.0-fix-doc-dest.patch
Patch3:		log4cpp-1.0-no-snprintf.patch
BuildRequires:	autoconf2.5
BuildRequires:  doxygen
BuildRequires:  libtool
BuildRequires:	multiarch-utils >= 1.0.3

%description
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

%package -n	%{libname}
Summary:	Log for C++ library
Group:		System/Libraries

%description -n	%{libname}
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

This package contains the shared library needed to run programs using log4cpp.

%package -n	%{develname}
Summary:	Development tools for Log for C++
Group:		Development/C++
Requires:	%{libname} >= %{version}
Provides:	liblog4cpp-devel = %{version}-%{release}
Provides:	log4cpp-devel = %{version}-%{release}

%description -n	%{develname}
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

This package contains the static libraries and header files needed for
development with %{libname}.

%package	doc
Summary:	HTML formatted API documention for Log for C++
Group:		Development/C++

%description	doc
The %{name}-doc package contains HTML formatted API documention generated
by the popular doxygen documentation generation tool.

%prep
%setup -q
%patch0 -p1 -b .gcc43
%patch1 -p1 -b .no-cflags
%patch2 -p1 -b .doc-dest
%patch3 -p1 -b .no-snprintf

# Delete non-free (but freely distributable) file under Artistic 1.0
# just to be sure we're not using it.
rm -rf src/snprintf.c

%build
libtoolize --copy --force; aclocal -I m4; autoconf; autoheader; automake --add-missing --copy
export LIBS="-lpthread"

%configure2_5x \
    --enable-doxygen
%make

%check
make check

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/log4cpp-config

%files -n %{libname}
%defattr(-,root,root,0755)
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root,0755)
%{_includedir}/*
%multiarch %{multiarch_bindir}/log4cpp-config

%attr(0755,root,root) %{_bindir}/log4cpp-config
%attr(0755,root,root) %{_libdir}/lib*.so
%attr(0644,root,root) %{_libdir}/*.*a
%attr(0644,root,root) %{_libdir}/pkgconfig/log4cpp.pc
%{_datadir}/aclocal/log4cpp.m4
%{_mandir}/*/*

%files doc
%defattr(-,root,root,0755)
%doc %{_docdir}/*

%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2011.0
+ Revision: 620250
- the mass rebuild of 2010.0 packages

* Fri Oct 23 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-0mdv2010.0
+ Revision: 459069
- 1.0
- sync with log4cpp-1.0-4.fc12.src.rpm
- added packaging fixes according to the mdv policy

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 0.3.4b-4mdv2008.1
+ Revision: 140932
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun May 27 2007 Pascal Terjan <pterjan@mandriva.org> 0.3.4b-4mdv2008.0
+ Revision: 31645
- rebuild
- Import log4cpp



* Tue Jan 31 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.3.4b-3mdk
- fix underquoted calls (P1)
- %%mkrel
- move %%configure to %%build
- don't wipe out buildroot in %%prep
- cosmetics

* Fri Jun 04 2004 Pascal Terjan <pterjan@mandrake.org> 0.3.4b-2mdk
- Rebuild

* Sun Oct 19 2003 Pascal Terjan <CMoi@tuxfamily.org> 0.3.4b-1mdk
- Mandrake adaptations
