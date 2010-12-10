%define major 4
%define libname %mklibname log4cpp %{major}
%define develname %mklibname log4cpp -d

Summary:	Log for C++
Name:		log4cpp
Version:	1.0
Release:	%mkrel 1
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Obsoletes:	%{mklibname log4cpp 3 -d}

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
rm -rf %{buildroot}

%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/log4cpp-config

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,0755)
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*
%doc AUTHORS COPYING INSTALL NEWS README THANKS ChangeLog

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
