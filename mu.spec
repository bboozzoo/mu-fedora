Name:           mu
Version:        0.9.9
Release:        3%{?dist}
Summary:        Tool for working with e-mail messages in Maildir format

License:        GPLv3
URL:            http://www.djcbsoftware.nl/code/mu
Source0:        http://mu0.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:  xapian-core-devel
BuildRequires:  libuuid-devel
BuildRequires:  emacs
BuildRequires:  glib2-devel
BuildRequires:  gmime-devel
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
BuildArch: noarch

%description -n emacs-mu4e-el
This package contains the elisp source files for mu4e. You do not need
to install this package to run mu4e. Install emacs-mu4e package instead.

%prep
%setup -q -D

%build
if [ ! -x ./configure ] ; then
   /usr/bin/autoreconf -if
fi
%configure --with-gui=none
# fix rpath, upstream distribues libtool from
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/info/dir

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
#%%{_emacs_sitestartdir}/*.elc

%files -n emacs-mu4e-el
%defattr(-,root,root,-)
%{_emacs_sitelispdir}/mu4e/*.el
#%%{_emacs_sitestartdir}/*.el

%post -n emacs-mu4e
/sbin/install-info %{_infodir}/mu4e.info.gz %{_infodir}/dir || :

%preun -n emacs-mu4e
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/mu4e.info.gz %{_infodir}/dir || :
fi


%changelog
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
