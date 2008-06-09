%define lib_major 3 
%define lib_name %mklibname log4cpp %{lib_major}

Name:		log4cpp
Version:	0.3.4b
Release:	%mkrel 4

Summary:	Log for C++
License:	LGPL
Group:		System/Libraries
Url:		http://log4cpp.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		log4cpp-0.3.4b-fix-underquoted-calls.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	autoconf2.5 doxygen

%description
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.

%package -n	%{lib_name}
Summary:	Log for C++ library
Group:		System/Libraries

%description -n	%{lib_name}
Log for C++ is a library of classes for flexible logging to files, syslog,
and other destinations. It is modeled after the Log for Java library and
stays as close to its API as is reasonable.
This package contains the library needed to run programs using log4cpp.

%package -n	%{lib_name}-devel
Summary:	Development tools for Log for C++
Group:		Development/C++
Requires:	%{lib_name} = %{version}
Provides:	liblog4cpp-devel  = %{version}

%description -n	%{lib_name}-devel
The %{lib_name}-devel package contains the static libraries and header files
needed for development with %lib_name.

%package	doc
Summary:	HTML formatted API documention for Log for C++
Group:		Development/C++

%description	doc
The %{name}-doc package contains HTML formatted API documention generated
by the popular doxygen documentation generation tool.

%prep
%setup -q
%patch0 -p1 -b .underquoted

%build
%configure2_5x --enable-doxygen 
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
mkdir -p $RPM_BUILD_ROOT/%_prefix/share/doc/
mv $RPM_BUILD_ROOT/%_prefix/doc/* $RPM_BUILD_ROOT/%_prefix/share/doc/

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(-,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*
%doc AUTHORS COPYING INSTALL NEWS README THANKS ChangeLog

%files -n %{lib_name}-devel
%defattr(-,root,root,755)
%{_datadir}/aclocal/log4cpp.m4
%{_includedir}/*
%{_mandir}/*/*
%attr(755,root,root) %{_bindir}/log4cpp-config
%attr(755,root,root) %{_libdir}/lib*.so
%attr(644,root,root) %{_libdir}/*.*a

%files doc
%defattr(-,root,root,755)
%doc %{_docdir}/*
