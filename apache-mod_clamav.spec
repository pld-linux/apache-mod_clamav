%define 	apxs		/usr/sbin/apxs
%define		mod_name	clamav
Summary:	An Apache virus scanning filter
Summary(pl.UTF-8):	Filtr skanera antywirusowego dla Apache'a
Name:		apache-mod_%{mod_name}
Version:	0.23
Release:	0.1
License:	GPL
Group:		Networking/Daemons/HTTP
Source0:	http://software.othello.ch/mod_clamav/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	32c7b285dfdff5d13371b92ebe73b352
Source1:	%{name}.conf
URL:		http://software.othello.ch/mod_clamav/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	apr-util-devel >= 1:1.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	clamav-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_proxy
Requires:	clamav
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_clamav is an Apache 2 filter which scans the content delivered by
the proxy module (mod_proxy) for viruses using the Clamav virus
scanning engine.

%description -l pl.UTF-8
mod_clamav to filtr dla serwera Apache 2 skanujący treści dostarczane
przez moduł proxy (mod_proxy) pod kątem wirusów przy użyciu silnika
skanera antywirusowego Clamav.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

CPPFLAGS="-I `/usr/bin/apr-1-config --includedir` -I `/usr/bin/apu-1-config --includedir`"
%configure \
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/32_mod_clamav.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog mod_clamav.html NEWS README TODO
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
