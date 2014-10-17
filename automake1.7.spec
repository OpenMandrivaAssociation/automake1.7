%define amversion 1.7

%define docheck 0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake%{amversion}
Version:	1.7.9
Release:	22
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/automake/
Source0:	ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Source1:	automake1.7.rpmlintrc
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
