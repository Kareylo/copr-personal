# Repackages the official prebuilt Linux tarball; nothing is compiled.
%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links none

%global appdir /opt/zen-browser

# The bundled NSS/NSPR/Mozilla libs are private to the app: don't advertise
# them to the system, and don't require them from it.
%global __provides_exclude_from ^%{appdir}/.*$
%global __requires_exclude ^(libclearkey|libfreeblpriv3|libgkcodecs|liblgpllibs|libmozavcodec|libmozavutil|libmozgtk|libmozinference|libmozsandbox|libmozsqlite3|libmozwayland|libnspr4|libnss3|libnssutil3|libonnxruntime|libplc4|libplds4|libsmime3|libsoftokn3|libssl3|libxul)\\.so.*$

Name:           zen-browser
Version:        1.24b
Release:        1%{?dist}
Summary:        Firefox-based browser focused on privacy and a calm workflow

License:        MPL-2.0
URL:            https://github.com/zen-browser/desktop
Source0:        %{url}/releases/download/%{version}/zen.linux-x86_64.tar.xz
Source1:        zen-browser.desktop
Source2:        zen
Source3:        policies.json

ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils

%description
Zen is a Firefox-based web browser with vertical tabs, workspaces and split
views.

This package repacks the official upstream Linux build under %{appdir}.
The built-in updater is disabled: updates come through dnf.

%prep
%setup -q -n zen

%install
mkdir -p %{buildroot}%{appdir}
cp -a . %{buildroot}%{appdir}/
install -Dpm0644 %{SOURCE3} %{buildroot}%{appdir}/distribution/policies.json

install -Dpm0755 %{SOURCE2} %{buildroot}%{_bindir}/zen
ln -s zen %{buildroot}%{_bindir}/zen-browser

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

for size in 16 32 48 64 128; do
    install -Dpm0644 browser/chrome/icons/default/default${size}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/zen-browser.png
done

%files
%{appdir}
%{_bindir}/zen
%{_bindir}/zen-browser
%{_datadir}/applications/zen-browser.desktop
%{_datadir}/icons/hicolor/*/apps/zen-browser.png

%changelog
* Tue Nov 03 2026 Kareylo <contact@kareylo.fr> - 1.24b-1
- Initial package, repacking the upstream x86_64 tarball
