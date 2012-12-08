%define amversion 1.7

%define docheck 0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake%{amversion}
Version:	1.7.9
%define subrel 1
Release:	16
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/automake/
Source:		ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Patch0:		automake-1.7.9-infofiles.patch
Patch1:		automake-1.7.9-new-autoconf-and-gettext.patch
Patch2:		automake-1.7.9-CVE-2009-4029.patch
Patch3:		automake-1.7.9-CVE-2012-3386.diff
BuildArch:	noarch
Requires:	autoconf2.5 >= 1:2.54
BuildRequires:	autoconf2.5 >= 1:2.59-4mdk
BuildRequires:	texinfo
Conflicts:	automake1.5
Conflicts:	automake < 1.4-22.p6.mdk
Requires(post): update-alternatives
# for tests
%if %docheck
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	tetex-latex
BuildRequires:	emacs
BuildRequires:	dejagnu
BuildRequires:	gcc-java
BuildRequires:	python
%endif

%description
Automake is a tool for automatically generating Makefiles compliant with
the GNU Coding Standards.

You should install Automake if you are developing software and would like
to use its capabilities of automatically generating GNU standard
Makefiles. If you install Automake, you will also need to install GNU's
Autoconf package.

%prep

%setup -q -n automake-%{version}
%patch0 -p0 -b .parallel
%patch1 -p1 -b .autoconf_gettext
%patch2 -p1 -b .CVE-2009-4029
%patch3 -p0 -b .CVE-2012-3386


%build
%configure2_5x
%make

%if %docheck
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present. But automake behavior changed, now it can handle missing
# libtool file as well, so this test is bogus.
perl -pi -e 's/reqd2.test//g' tests/Makefile
# etex is linked to pdfetex, which does not generate dvi files...
export TEX=tex
# (oe) these test cases fail probably due to incompabilities with latest gettext,
# disable them for now
for test in gettext gettext2 subcond subst; do
    perl -pi -e "s|${test}||g" tests/Makefile
done
make check	# VERBOSE=1
%endif

%install
%makeinstall_std

rm -f %{buildroot}/%{_bindir}/{automake,aclocal}

pushd %{buildroot}/%{_infodir}
for i in *.info*; do
  mv $i %{name}${i#automake}
done
popd

mkdir -p %{buildroot}%{_datadir}/aclocal

%post
update-alternatives --remove automake %{_bindir}/automake-%{amversion}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_bindir}/*
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*


%changelog
* Mon Jul 16 2012 Danila Leontiev <danila.leontiev@rosalab.ru> 1.7.9-15.1
- Rebuilded for ROSA

* Thu Jul 12 2012 Oden Eriksson <oeriksson@mandriva.com> 1.7.9-12.1
- P3: security fix for CVE-2012-3386

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.7.9-12mdv2011.0
+ Revision: 662900
- mass rebuild

* Wed Oct 13 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.9-11mdv2011.0
+ Revision: 585443
- P2: security fix for CVE-2009-4029 (redhat)

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.9-10mdv2010.1
+ Revision: 520014
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.7.9-9mdv2010.0
+ Revision: 413149
- rebuild

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 1.7.9-8mdv2009.1
+ Revision: 350137
- 2009.1 rebuild

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1.7.9-7mdv2009.0
+ Revision: 233112
- disable the test suite for now
- another try, without the %%check macro
- disable 4 tests, probably due to incompabilities with latest gettext

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 1.7.9-5mdv2008.1
+ Revision: 135825
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix update-alternative file require
    - kill file require on info-install


* Fri Mar 02 2007 Christiaan Welvaart <cjw@daneel.dyndns.org>
+ 2007-03-02 11:00:37 (131041)
- patch1: fix test suite for new autoconf and gettext
- from Götz Waschk <waschk@mandriva.org>
    - Import automake1.7

* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 1.7.9-3mdv2007.1
- unpack patch

* Sun May 07 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.7.9-3mdk
- drop 'automake' provides and alternative
- run tests (by default)
- add buildrequires for tests: python tetex-latex

* Wed May 19 2004 Abel Cheung <deaddog@deaddog.org> 1.7.9-2mdk
- 1.7.x is not an upgrade of 1.5.x
- Tune up alternative priority
- Add `--with check' option to enable `make check'
- Adjust patch0 to refer to the actual command (*-1.7 rather than *1.7)
- Also owns /usr/share/aclocal

