%define major 5
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Name:          log4cpp
Version:       1.1.4
Release:       1
Summary:       C++ logging library
Group:         Development/C++
License:       LGPL
Url:           http://sourceforge.net/projects/log4cpp/
Source0:       https://sourceforge.net/projects/log4cpp/files/log4cpp-1.1.x%20%28new%29/log4cpp-1.1/%{name}-%{version}.tar.gz
# Fix errors when compiling with gcc >= 4.3
Patch0:        log4cpp-1.0-gcc43.patch
# Don't put build cflags in .pc
Patch1:        log4cpp-1.0-remove-pc-cflags.patch
# Install docs into DESTDIR
Patch2:        log4cpp-1.0-fix-doc-dest.patch
# Don't try to build snprintf.c
Patch3:        log4cpp-1.0-no-snprintf.patch
Patch4:        log4cpp-1.0-automake-1.13.patch
Patch5:	       log4cpp-1.0-pthread.patch

BuildRequires: doxygen

%description
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

%package -n %{libname}
Group:		System/Libraries
Summary:	Shared libraries for %{name}
Obsoletes:	%{name} < 1.0-2

%description -n %{libname}
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

%package -n %{develname}
Group:         Development/C++
Summary:       The %{name} development libraries and headers
Requires:      %{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < 1.0-2

%description -n %{develname}
%{name} - Log library for C++.

This package contains development libraries and headers for %{name}.

%package doc
Group:         Documentation
Summary:       HTML formatted API documention for Log for C++
BuildArch:	noarch

%description doc
%{name} - Log library for C++.

This package contains the development documentation for %{name}.

%prep
%setup -q -n %{name}
%autopatch -p1
# Delete non-free (but freely distributable) file under Artistic 1.0
# just to be sure we're not using it.
rm -rf src/snprintf.c
#Convert line endings.
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog

%build
export PTHREAD_LIBS=-lpthread
autoreconf -fi -Im4
%configure --disable-static
%make_build

%install
%make_install
mv %{buildroot}%{_docdir}/log4cpp-* rpmdocs

find %{buildroot} -name '*.la' -delete

%files -n %{libname}
%{_libdir}/liblog4cpp.so.%{major}
%{_libdir}/liblog4cpp.so.%{major}.*
%doc ChangeLog COPYING

%files -n %{develname}
%{_bindir}/log4cpp-config
%{_includedir}/log4cpp
%{_libdir}/liblog4cpp.so
%{_libdir}/pkgconfig/log4cpp.pc
%{_datadir}/aclocal/log4cpp.m4
%{_mandir}/man3/log4cpp*

%files doc
%doc rpmdocs/*
