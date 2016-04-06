# git SHA-1 of 0.9.16 tag
%global commit 1c0bfe81a776b7f6e24f0ffe4ff3433f86de116c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global owner djcb

%global guile_pkgconf %(pkg-config --list-all | grep guile | sed -e 's! .*$!!g')
%global guile_sitedir %(pkg-config --variable=sitedir %{guile_pkgconf})

Name:           mu
Version:        0.9.16
Release:        1%{?dist}
Summary:        Tool for working with e-mail messages in Maildir format

License:        GPLv3
URL:            http://www.djcbsoftware.nl/code/mu
Source0:        https://github.com/%{owner}/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
BuildRequires:  xapian-core-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmime-2.6)
BuildRequires:  pkgconfig(guile-2.0)
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
nice Emacs interface provided in emacs-mu4e package. Mu facilities can
also be accessed from Scheme using provided bindings for GNU Guile.

%package -n emacs-mu4e
Summary: GNU Emacs support for mu
BuildRequires:  emacs
Requires: emacs(bin) >= %{_emacs_version}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description -n emacs-mu4e
mu4e is an emacs client for mu, similar to wanderlust. It's aim is to
make the use of Maildir e-mail message convenient under Emacs.

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
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/info/dir
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a
# mug is not shipped
rm -f %{buildroot}%{_datadir}/man/man1/mug.1.gz

%check
make check

%files
%doc COPYING
%{_bindir}/mu
%{_datadir}/man/man*/*
%{_libdir}/libguile-mu.so*
%{guile_sitedir}/*
%{_datadir}/info/mu-guile.*.gz
%dir %{_datadir}/mu
%dir %{_datadir}/mu/scripts
%{_datadir}/mu/scripts/*
%{_datadir}/doc/%{name}
%{_datadir}/doc/%{name}/NEWS.org

%files -n emacs-mu4e
%dir %{_emacs_sitelispdir}/mu4e
%{_emacs_sitelispdir}/mu4e/*.elc
%{_emacs_sitelispdir}/mu4e/*.el
%{_datadir}/info/mu4e.*.gz
%{_datadir}/doc/%{name}/mu4e-about.org

%post -n emacs-mu4e
/sbin/install-info %{_infodir}/mu4e.info.gz %{_infodir}/dir || :

%preun -n emacs-mu4e
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/mu4e.info.gz %{_infodir}/dir || :
fi

%post
/sbin/install-info %{_infodir}/mu-guile.info.gz %{_infodir}/dir || :
/sbin/ldconfig

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/mu-guile.info.gz %{_infodir}/dir || :
fi

%postun -p /sbin/ldconfig

%changelog
* Wed Apr  6 2016 Maciek Borzęcki <maciek.borzecki@gmail.com> - 0.9.16-1
- Update to mu 0.9.16

* Sat Dec 13 2014 Maciek Borzęcki <maciek.borzecki@gmail.com> - 0.9.11-2
- Updated according to review comments.

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
