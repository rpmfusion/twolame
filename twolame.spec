Name:		twolame
Version:	0.3.12
Release:	2%{?dist}
Summary:	TwoLAME is an optimised MPEG Audio Layer 2 encoding library based on tooLAME
Group:		Applications/Multimedia
License:	LGPLv2+
URL:		http://www.twolame.org/
Source:		http://downloads.sourceforge.net/twolame/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libsndfile-devel
BuildRequires:	libtool

%description
TwoLAME is an optimised MPEG Audio Layer 2 encoding library based on tooLAME,
which in turn is based heavily on
- the ISO dist10 code
- improvement to algorithms as part of the LAME project (www.sulaco.org/mp3)

This package contains the command line frontend.
                                                                                
%package libs
Summary:	TwoLAME is an optimised MPEG Audio Layer 2 encoding library based on tooLAME
Group:		System Environment/Libraries
Obsoletes:	%{name} < 0.3.12-1

%description libs
TwoLAME is an optimised MPEG Audio Layer 2 encoding library based on tooLAME,
which in turn is based heavily on
- the ISO dist10 code
- improvement to algorithms as part of the LAME project (www.sulaco.org/mp3)

This package contains the shared library.

%package devel
Summary:	Development tools for TwoLAME applications
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the header files and documentation
needed to develop applications with TwoLAME.

%prep
%setup -q
# convert manpage to UTF8
pushd doc
iconv -f iso8859-1 -t utf8 %{name}.1 > %{name}.1.utf && mv %{name}.1.utf %{name}.1
# fix HTML docs line endings
for file in html/*.html ; do
	tr -d '\r' <$file >$file.unix && mv $file.unix $file
done
popd

%build
autoreconf -f -i
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_docdir}

%clean 
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README TODO
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files libs
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/lib%{name}.so.*

%files devel
%defattr(644,root,root,755)
%doc doc/api.txt doc/html doc/psycho.txt doc/vbr.txt
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h

%changelog
* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.3.12-2
- rebuild

* Sun Jan 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.3.12-1
- updated to 0.3.12
- updated source URL
- split off libs to avoid multilib conflicts
- move docs processing to prep to avoid problems with shortcut builds
- update license tag

* Thu May 03 2007 Dominik Mierzejewski <rpm@greysector.net> 0.3.10-1
- updated to 0.3.10
- removed redundant BRs

* Wed Nov 01 2006 Dominik Mierzejewski <rpm@greysector.net> 0.3.8-1
- updated to 0.3.8
- rebuild autofiles to get rid of rpath
- disable static library build
- fix manpage encoding
- fix HTML docs line endings

* Sun Mar 12 2006 Dominik Mierzejewski <rpm@greysector.net> 0.3.6-1
- updated to 0.3.6

* Tue Jan 24 2006 Dominik Mierzejewski <rpm@greysector.net> 0.3.5-1
- updated to 0.3.5
- simplified package layout
- FE/livna compliance

* Sun Aug 21 2005 Dominik Mierzejewski <rpm@greysector.net>
- initial package
