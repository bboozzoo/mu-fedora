# git SHA-1 of 0.9.11 tag
%global commit e434ea7680fb89c972b2c71783fea12c4c88a129
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%define owner djcb

%global guile_pkgconf %(pkg-config --list-all | grep guile | sed -e 's! .*$!!g')
%global guile_sitedir %(pkg-config --variable=sitedir %{guile_pkgconf})

Name:           mu
Version:        0.9.11
Release:        1%{?dist}
Summary:        Tool for working with e-mail messages in Maildir format

License:        GPLv3
URL:            http://www.djcbsoftware.nl/code/mu
Source0:        https://github.com/%{owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
BuildRequires:  xapian-core-devel
# unlisted dependency for xapian-core-devel, see
# https://bugzilla.redhat.com/show_bug.cgi?id=1173099
BuildRequires:  libuuid-devel

BuildRequires:  emacs
BuildRequires:  glib2-devel
BuildRequires:  gmime-devel
BuildRequires:  guile-devel
BuildRequires:  zlib-devel
BuildRequires:  texinfo
BuildRequires:  autoconf automake libtool pkgconfig
Requires(post): info
Requires(preun): info

%description
mu is a tool for dealing with e-mail messages stored in the
Maildir-format, on Unix-like systems. mu's main purpose is to help you
to find the messages you need, quickly; in addition, it allows you to
view messages, extract attachments, create new maildirs, etc. mu has a
nice Emacs interface provided in emacs-mu4e package.

%package -n emacs-mu4e
Summary: GNU Emacs support for mu
Requires: emacs(bin) >= %{_emacs_version}
Requires: mu = %{version}-%{release}
BuildArch: noarch

%description -n emacs-mu4e
mu4e is an emacs client for mu, similar to wanderlust. It's aim is to
make the use of Maildir e-mail message convenient under Emacs.

%package -n emacs-mu4e-el
Summary: GNU Emacs support for mu. Source files
Requires: emacs
Requires: mu = %{version}-%{release}
Requires: emacs-mu4e = %{version}-%{release}
BuildArch: noarch

%description -n emacs-mu4e-el
This package contains the elisp source files for mu4e. You do not need
to install this package to run mu4e. Install emacs-mu4e package instead.

%package -n guile-mu
Summary: Guile bindings for mu library
Requires: mu = %{version}-%{release}

%description -n guile-mu
The package contains guile bindings for mu.


%package -n guile-mu-devel
Summary: Guile bindings for mu library 
Requires: guile-mu = %{version}-%{release}

%description -n guile-mu-devel
The package contains development files mu guile bindings.

%prep
%setup -q -D -n %{name}-%{commit}

%build
if [ ! -x ./configure ] ; then
   /usr/bin/autoreconf -if
fi
EMACS=/usr/bin/emacs %configure --enable-mu4e --enable-guile --disable-gtk
# fix rpath, upstream distribues libtool from
# sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
# sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/info/dir
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/mu
%{_datadir}/man/man*/*.gz

%files -n emacs-mu4e
%defattr(-,root,root,-)
%dir %{_emacs_sitelispdir}/mu4e
%{_emacs_sitelispdir}/mu4e/*.elc
%{_datadir}/info/mu4e.*.gz

%files -n emacs-mu4e-el
%defattr(-,root,root,-)
%{_emacs_sitelispdir}/mu4e/*.el

%post -n emacs-mu4e
/sbin/install-info %{_infodir}/mu4e.info.gz %{_infodir}/dir || :

%preun -n emacs-mu4e
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/mu4e.info.gz %{_infodir}/dir || :
fi

%files -n guile-%{name}
%{_libdir}/libguile-mu.so.*
%{guile_sitedir}/*
%{_datadir}/info/mu-guile.*.gz
%{_datadir}/mu/scripts/*

%post -n guile-%{name}
/sbin/install-info %{_infodir}/mu-guile.info.gz %{_infodir}/dir || :
/sbin/ldconfig

%preun -n guile-%{name}
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/mu-guile.info.gz %{_infodir}/dir || :
fi

%postun -n guile-mu
/sbin/ldconfig

%files -n guile-%{name}-devel
%{_libdir}/libguile-mu.so

%changelog
* Thu Dec 11 2014 Maciek Borzecki <maciek.borzecki@gmail.com> - 0.9.11-1
- Update to version 0.9.11

* Wed May 22 2013 Matt Ford <matt@dancingfrog.co.uk> - 0.9.9.5-1
- Updated to latest version 0.9.9.5

* Fri Nov  9 2012 Maciek Borzecki <maciek.borzecki@gmail.com> - 0.9.9-4
- Make emacs-mu4e a dependency for emacs-mu4e-el

* Mon Nov  5 2012 Maciek Borzecki <maciek.borzecki@gmail.com> - 0.9.9-3
- Fix mu4e elisp files directory ownership

* Sun Oct 21 2012 Maciek Borzecki <maciek.borzecki@gmail.com> - 0.9.9-2
- Addressed package review issues

* Fri Oct 19 2012 Maciek Borzecki <maciek.borzecki@gmail.com> - 0.9.9-1
- Updating to release 0.9.9

* Fri Oct 12 2012 Maciek Borzecki <maciek@corsair> - 0.9.8.5-1
- Update to mu v0.9.8.5

* Sun May 13 2012 Maciek Borzecki <maciek.borzecki@gmail.com> - 0.9.8.4-1
- Initial packaging of 0.9.8.4
