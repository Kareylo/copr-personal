%global debug_package %{nil}

Name:           obsidian
Version:        1.15.0
Release:        3%{?dist}
Summary:        Knowledge base application for Markdown notes

License:        LicenseRef-Obsidian
URL:            https://github.com/obsidianmd/obsidian-releases
Source0:        %{url}/releases/download/v%{version}/obsidian_%{version}_amd64.deb
Source1:        obsidian

ExclusiveArch:  x86_64
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  xz
Requires:       at-spi2-core
Requires:       gtk3
Requires:       libnotify
Requires:       libsecret
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       nss
Requires:       xdg-utils

%description
Obsidian is a knowledge base application that works on top of a local folder
of plain text Markdown files.

This package repacks the official upstream Debian package and installs the
bundled Electron application under /opt/Obsidian.

%prep
%setup -q -T -c -n %{name}-%{version}
cp -p %{SOURCE0} .
ar x obsidian_%{version}_amd64.deb
tar -xJf data.tar.xz

%install
cp -a opt %{buildroot}/
mkdir -p %{buildroot}%{_datadir}
cp -a usr/share/. %{buildroot}%{_datadir}/
sed -i 's|/opt/Obsidian/obsidian|obsidian|g' \
  %{buildroot}%{_datadir}/applications/md.obsidian.Obsidian.desktop
install -Dpm0755 %{SOURCE1} %{buildroot}%{_bindir}/obsidian
install -Dpm0644 %{buildroot}/opt/Obsidian/LICENSE.electron.txt \
  %{buildroot}%{_licensedir}/%{name}/LICENSE.electron.txt
install -Dpm0644 %{buildroot}/opt/Obsidian/LICENSES.chromium.html \
  %{buildroot}%{_licensedir}/%{name}/LICENSES.chromium.html

%files
%{_bindir}/obsidian
/opt/Obsidian
%{_datadir}/applications/md.obsidian.Obsidian.desktop
%{_datadir}/icons/hicolor/*/apps/obsidian.png
%{_datadir}/mime/packages/obsidian.xml
%doc %{_docdir}/obsidian/changelog.gz
%license %{_licensedir}/%{name}/LICENSE.electron.txt
%license %{_licensedir}/%{name}/LICENSES.chromium.html

%changelog
* Wed Apr 08 2026 Kristian Tagesen <kristian@example.invalid> - 1.12.7-3
- Package the upstream Debian changelog installed under %%{_docdir}

* Wed Apr 08 2026 Kristian Tagesen <kristian@example.invalid> - 1.12.7-2
- Fix Debian data installation paths

* Wed Apr 08 2026 Kristian Tagesen <kristian@example.invalid> - 1.12.7-1
- Initial package
