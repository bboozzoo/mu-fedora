Name:           mu
Version:        0.9.8.4
Release:        1%{?dist}
Summary:        Tool for working with e-mail messages in Maildir format

License:        GPLv3
URL:            http://www.djcbsoftware.nl/code/mu
Source0:        http://mu0.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:  xapian-core-devel
BuildRequires:  libuuid-devel
BuildRequires:  emacs
BuildRequires:  glib2-devel
Requires:       xapian-core-libs libuuid glib2
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
%configure --with-gui=none
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir


%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/mu
%{_datadir}/man/man*
%{_datadir}/info/mu4e.info*

%files -n emacs-mu4e
%defattr(-,root,root,-)
%{_emacs_sitelispdir}/mu4e/*.elc
#%%{_emacs_sitestartdir}/*.elc

%files -n emacs-mu4e-el
%defattr(-,root,root,-)
%{_emacs_sitelispdir}/mu4e
#%%{_emacs_sitestartdir}/*.el

%post -n emacs-mu4e
/sbin/install-info %{_infodir}/mu4e.info.gz %{_infodir}/dir || :

%preun -n emacs-mu4e
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/mu4e.info.gz %{_infodir}/dir || :
fi


%changelog
* Sun May 13 2012 Maciek Borzecki <maciek.borzecki@gmail.com> - 0.9.8.4-1
- Initial packaging of 0.9.8.4

