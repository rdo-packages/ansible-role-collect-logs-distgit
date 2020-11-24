# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%global srcname ansible_role_collect_logs
%global rolename ansible-role-collect-logs

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           %{rolename}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Ansible role to collect the logs from a TripleO/OSP based deployment of OpenStack

Group:          System Environment/Base
License:        ASL 2.0
URL:            https://git.openstack.org/cgit/openstack/ansible-role-collect-logs
Source0:        https://tarballs.openstack.org/%{rolename}/%{rolename}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{rolename}/%{rolename}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

BuildRequires:  python3dist(ansible)
BuildRequires:  git-core
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  /usr/bin/pathfix.py

# Handle python2 exception
%if %{pyver} == 2
Requires: ansible
%else
Requires: python3dist(ansible)
%endif

%description

Ansible role to collect the logs from a TripleO/OSP based deployment of OpenStack

%prep
%autosetup -n %{rolename}-%{upstream_version} -S git


%build
%pyver_build


%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%pyver_install
# Fix shebang
pathfix.py -pni "%{__python%{pyver}} %{py%{pyver}_shbang_opts}" %{buildroot}/usr/share/ansible/roles/collect-logs/library/flatten_nested_dict.py

%check
ROLE_NAME="collect-logs"
ansible-galaxy list -p %{buildroot}/usr/share/ansible/roles $ROLE_NAME|grep -v "$ROLE_NAME was not found"

%files
%doc README*
%license LICENSE
%{pyver_sitelib}/%{srcname}-*.egg-info
%{_datadir}/ansible/


%changelog
* Tue Nov 24 2020 Chandan Kumar <chkumar@redhat.com> 1.0.0-1
- Bump to version 1.0.0
