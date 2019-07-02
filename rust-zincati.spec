# Generated by rust2rpm 10
%bcond_without check
%global __cargo_skip_build 0

%global crate zincati

Name:           rust-%{crate}
Version:        0.0.2
Release:        5%{?dist}
Summary:        Update agent for Fedora CoreOS

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            https://crates.io/crates/zincati
Source:         %{crates_source}
# Initial patched metadata
Patch0:         zincati-fix-metadata.diff

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  systemd-rpm-macros

%global _description %{expand:
Update agent for Fedora CoreOS.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}

%description -n %{crate} %{_description}

%files       -n %{crate}
%{_bindir}/zincati
%doc README.md
%license COPYRIGHT LICENSE
%dir %{_prefix}/lib/%{crate}
%dir %{_prefix}/lib/%{crate}/config.d
%{_prefix}/lib/%{crate}/config.d/50-fedora-coreos-cincinnati.toml
%attr(0775, zincati, zincati) %dir /run/%{crate}
%attr(0775, zincati, zincati) %dir /run/%{crate}/config.d
%attr(0770, zincati, zincati) %dir /run/%{crate}/private
# TODO: add /run/zincati/public once created in zincati.conf tmpfile.
%dir %{_sysconfdir}/%{crate}
%dir %{_sysconfdir}/%{crate}/config.d
%{_unitdir}/zincati.service
%{_sysusersdir}/50-zincati.conf
%{_tmpfilesdir}/zincati.conf

%pre         -n %{crate}
%sysusers_create_package %{crate} 50-zincati.conf
%tmpfiles_create_package %{crate} zincati.conf

%post        -n %{crate}
%systemd_post zincati.service

%preun       -n %{crate}
%systemd_preun zincati.service

%postun      -n %{crate}
%systemd_postun_with_restart zincati.service

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install
install -Dpm0644 -t %{buildroot}%{_prefix}/lib/%{crate}/config.d \
  dist/config.d/*.toml
mkdir -p %{buildroot}/run/%{crate}/config.d
mkdir -p %{buildroot}/run/%{crate}/private
mkdir -p %{buildroot}%{_sysconfdir}/%{crate}/config.d
install -Dpm0644 -t %{buildroot}%{_unitdir} \
  dist/systemd/system/*.service
install -Dpm0644 -t %{buildroot}%{_sysusersdir} \
  dist/sysusers.d/*.conf
install -Dpm0644 -t %{buildroot}%{_tmpfilesdir} \
  dist/tmpfiles.d/*.conf

%if %{with check}
%check
%cargo_test
%endif

%changelog
* Tue Jul 02 2019 Robert Fairley <rfairley@redhat.com> - 0.0.2-5
- Add missing owned directories, tidy owned files list

* Tue Jul 02 2019 Robert Fairley <rfairley@redhat.com> - 0.0.2-4
- Add runtime directories ownership by zincati sysuser

* Wed Jun 26 2019 Robert Fairley <rfairley@redhat.com> - 0.0.2-3
- Patch to use liboverdrop-0.0.2

* Wed Jun 26 2019 Robert Fairley <rfairley@redhat.com> - 0.0.2-2
- Fix specfile log, and macro in comment

* Wed Jun 26 2019 Robert Fairley <rfairley@redhat.com> - 0.0.2-1
- Update to 0.0.2

* Tue Jun 18 13:38:53 UTC 2019 Robert Fairley <rfairley@redhat.com> - 0.0.1-1
- Initial package
