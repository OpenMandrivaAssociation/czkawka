%bcond_without check
%global __cargo_skip_build 0

%global uuid com.github.qarmin.czkawka
%global pkgname czkawka
%global guiapp gui
%global orbapp orbtk
%global cliapp cli

Name:           czkawka
Version:        2.3.2
Release:        1
Summary:        Multi functional app to find duplicates, empty folders etc.

# Upstream license specification: MIT
License:        MIT
URL:            https://github.com/qarmin/czkawka
Source0:        https://github.com/qarmin/czkawka/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  rust-packaging
BuildRequires:  rust
BuildRequires:  rust-src
BuildRequires:  cargo
BuildRequires:	cargo-c
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gdk-3.0) >= 3.22
BuildRequires: hicolor-icon-theme

BuildRoot: %{_tmppath}/%{name}-%{version}-build


%global srcroot %{_sourcedir}/%{pkgname}-%{version}

%description
Czkawka is simple, fast and easy to use alternative to Fslint, written in Rust.
This is my first ever project in Rust so probably a lot of things are not being written in the most optimal way.

%package     -n %{pkgname}-%{cliapp}
Summary:        CLI frontend of Czkawka

%description -n %{pkgname}-%{cliapp}
CLI frontent of Czkawka

%files       -n %{pkgname}-%{cliapp}
%license LICENSE
%{_bindir}/%{pkgname}_%{cliapp}
%{_bindir}/%{pkgname}


%package     -n %{pkgname}-%{guiapp}
Summary:        GTK frontend of Czkawka

%description -n %{pkgname}-%{guiapp}
GTK frontent of Czkawka

%files       -n %{pkgname}-%{guiapp}
%license LICENSE
%{_bindir}/%{pkgname}_%{guiapp}
%{_datadir}/icons/hicolor/512x512/apps/%{uuid}.png
%{_datadir}/icons/hicolor/scalable/apps/%{uuid}.svg
%{_datadir}/applications/%{uuid}.desktop


%package     -n %{pkgname}-%{orbapp}
Summary:        Orbtk frontend of Czkawka

%description -n %{pkgname}-%{orbapp}
Orbtk frontend of Czkawka

%files       -n %{pkgname}-%{orbapp}
%license LICENSE
%{_bindir}/%{pkgname}_%{guiapp}_%{orbapp}

%package     -n %{pkgname}-doc
Summary:        Documentation of Czkawka
BuildArch:      noarch

%description -n %{pkgname}-doc
Documentation of Czkawka

%files       -n %{pkgname}-doc
%license LICENSE
%doc README.md
%doc Instruction.md
%doc Changelog.md

%prep
%autosetup -p1

%cargo_prep

%build
#cargo_build

cargo build --release --bin czkawka_gui
cargo build --release --bin czkawka_cli

%install
#cargo_install
mkdir -p %{buildroot}%{_bindir}/
install -Dm755 ./target/release/%{pkgname}_%{cliapp} %{buildroot}%{_bindir}
install -Dm755 ./target/release/%{pkgname}_%{guiapp} %{buildroot}%{_bindir}
install -Dm755 ./target/release/%{pkgname}_%{guiapp}_%{orbapp} %{buildroot}%{_bindir}
ln -s %{_bindir}%{pkgname}_%{cliapp} %{buildroot}%{_bindir}/%{pkgname}
install -Dm644 ./icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{uuid}.png
install -Dm644 ./icon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{uuid}.svg
#install -Dm644 ./pkgs/%{uuid}.desktop %{buildroot}%{_datadir}/applications/%{uuid}.desktop
%if 0%{?suse_version}
%suse_update_desktop_file -c %{uuid} Czkawka "Multi functional app to clean OS which allow to find duplicates, empty folders, similar files etc." %{pkgname}_%{guiapp} %{uuid} System
%endif

%if %{with check}
%check
%cargo_test
%endif
