%define version 1.7.9
%define release %mkrel 4

%define amversion 1.7

%define docheck 1
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		automake%{amversion}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source:		ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Patch0:		automake-1.7.9-infofiles.patch
Patch1:		automake-1.7.9-new-autoconf-and-gettext.patch
URL:		http://sources.redhat.com/automake/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch

Requires:	autoconf2.5 >= 1:2.54
BuildRequires:	autoconf2.5 >= 1:2.59-4mdk
BuildRequires:	texinfo
Conflicts:	automake1.5
Conflicts:	automake < 1.4-22.p6.mdk
Requires(post):	info-install /usr/sbin/update-alternatives
Requires(preun):	info-install

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
make check	# VERBOSE=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

rm -f $RPM_BUILD_ROOT/%{_bindir}/{automake,aclocal}

pushd $RPM_BUILD_ROOT/%{_infodir}
for i in *.info*; do
  mv $i %{name}${i#automake}
done
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %name.info
update-alternatives --remove automake %{_bindir}/automake-%{amversion}

%preun
%_remove_install_info %name.info

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_bindir}/*
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*

