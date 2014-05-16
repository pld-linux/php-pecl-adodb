%define		php_name	php%{?php_suffix}
%define		modname	adodb
%define		ver		%(echo %{version} | tr -d .)
Summary:	ADOdb PHP extension
Name:		%{php_name}-pecl-%{modname}
Version:	5.0.4
Release:	5
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://phplens.com/lens/dl/adodb-ext-%{ver}.zip
# Source0-md5:	4efb3fc1f5a347f20be9222885779688
Patch0:		php53.patch
URL:		http://adodb.sourceforge.net/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.650
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-adodb < 5.0.4-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ADOdb PHP extension provides up to 100% speedup by replacing parts of
ADOdb with C code. ADOdb will auto-detect if this extension is
installed and use it automatically.

%prep
%setup -qc
mv %{modname}-%{ver}/* .
%undos -f c,txt
%patch0 -p1

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS README.txt
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
