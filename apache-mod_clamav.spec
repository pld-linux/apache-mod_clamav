%define 	apxs		/usr/sbin/apxs
%define		mod_name	clamav
Summary:	An Apache virus scanning filter
Summary(pl):	Filtr skanera antywirusowego dla Apache'a
Name:		apache-mod_%{mod_name}
Version:	0.21
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://software.othello.ch/mod_clamav/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	98bd0d8628be8ddeae21da6623e57d20
Source1:	%{name}.conf
Patch0:		%{name}-libtool-tag.patch
URL:		http://software.othello.ch/mod_clamav/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	clamav-devel
BuildRequires:	libtool
Requires:	apache >= 2
Requires:	apache-mod_proxy
Requires:	clamav
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)
%define		_libexecdir	%{_libdir}/apache

%description
mod_clamav is an Apache 2 filter which scans the content delivered by
the proxy module (mod_proxy) for viruses using the Clamav virus
scanning engine.

%description -l pl
mod_clamav to filtr dla serwera Apache 2 skanuj±cy tre¶ci dostarczane
przez modu³ proxy (mod_proxy) pod k±tem wirusów przy u¿yciu silnika
skanera antywirusowego Clamav.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p0

%{__perl} -pi -e 's/(-module)/$1 -avoid-version/' Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

CPPFLAGS="-I `/usr/bin/apr-config --includedir` -I `/usr/bin/apu-config --includedir`"
%configure \
	--with-apxs=%{apxs}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

CFG="$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf"
install %{SOURCE1} ${CFG}/32_mod_clamav.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog mod_clamav.html NEWS README TODO
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd.conf/32_mod_clamav.conf
%attr(755,root,root) %{_libexecdir}/mod_%{mod_name}.so
