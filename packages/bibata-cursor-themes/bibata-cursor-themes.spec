%global         source_name Bibata_Cursor
%global         debug_package %{nil}

Name:           bibata-cursor-themes
Version:        2.0.7
Release:        1%{?dist}
Summary:        OpenSource, Compact and Material Designed Cursor Set

License:        GNU General Public License v3.0
URL:            https://github.com/ful1e5/Bibata_Cursor
Source:         %{url}/archive/v%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/bitmaps.zip

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-pip

Requires:       gtk3

%description
OpenSource, Compact and Material Designed Cursor Set

%prep
%autosetup -c
%autosetup -T -D -a 1

mv bitmaps %{source_name}-%{version}

%build
export PATH="/builddir/.local/bin:$PATH"
pip install clickgen

cd %{source_name}-%{version}

declare -A normal_names
normal_names["Bibata-Modern-Amber"]="Yellowish and rounded edge Bibata cursors"
normal_names["Bibata-Modern-Classic"]="Black and rounded edge Bibata cursors"
normal_names["Bibata-Modern-Ice"]="White and rounded edge Bibata cursors"
normal_names["Bibata-Original-Amber"]="Yellowish and sharp edge Bibata cursors"
normal_names["Bibata-Original-Classic"]="Black and sharp edge Bibata cursors"
normal_names["Bibata-Original-Ice"]="White and sharp edge Bibata cursors"

for key in "${!normal_names[@]}"; do
    comment="${normal_names[$key]}"
    ctgen configs/normal/x.build.toml -p x11 -d "bitmaps/$key" -n "$key" -c "$comment"
done

declare -A right_names
right_names["Bibata-Modern-Amber-Right"]="Yellowish and rounded edge right-hand Bibata cursors"
right_names["Bibata-Modern-Classic-Right"]="Black and rounded edge right-hand Bibata cursors"
right_names["Bibata-Modern-Ice-Right"]="White and rounded edge right-hand Bibata cursors"
right_names["Bibata-Original-Amber-Right"]="Yellowish and sharp edge right-hand Bibata cursors"
right_names["Bibata-Original-Classic-Right"]="Black and sharp edge right-hand Bibata cursors"
right_names["Bibata-Original-Ice-Right"]="White and sharp edge right-hand Bibata cursors"

for key in "${!right_names[@]}"; do
    comment="${right_names[$key]}"
    ctgen configs/right/x.build.toml -p x11 -d "bitmaps/$key" -n "$key" -c "$comment"
done

%install
%__rm -rf %{buildroot}
%__mkdir -p %{buildroot}%{_datadir}/icons
for theme in $(ls %{_builddir}/%{name}-%{version}/%{source_name}-%{version}/themes); do
    %__mv %{_builddir}/%{name}-%{version}/%{source_name}-%{version}/themes/${theme} %{buildroot}%{_datadir}/icons
    %__chmod 0755 %{buildroot}%{_datadir}/icons/${theme}
done

%clean
%__rm -rf %{buildroot}

%files
%license %{source_name}-%{version}/LICENSE
%doc %{source_name}-%{version}/README.md
%{_datadir}/icons/*

%changelog
* Tue Jun 18 2024 Peter Wu <peterwu@hotmail.com> - 2.0.7-1
- New Release - v2.0.7
