%bcond_without check
%global __cargo_skip_build 0

%global uuid com.github.qarmin.czkawka
%global pkgname czkawka
%global guiapp gui
%global orbapp orbtk
%global cliapp cli

# Do not upgrade without testing!
# Looks like compiling with system provided rust packages is not posible at this time. 
# Online installation is not possible too due strange errors:
# "error: no matching package named `audiotags` found
# location searched: registry `https://github.com/rust-lang/crates.io-index`"
# For some reason this crates can't be found. So as workaround, we can create own vendor pack.
# Download czkawka .tar.gz source, unpack it, cd and install 'dnf install cargo-vendor'
# Then inside czkawka dir (or any other cargo/rust project) run in terminal command: 'cargo vendor'
# This create new dir called vendor and download here all needed crates dependencies.
# When process finish, compress it as vendor.tar.xz and upload to file-store. Place here as Source1.

Summary:	Multi functional app to find duplicates, empty folders etc.
Name:		czkawka
Version:	5.0.0
Release:	1
# Upstream license specification: MIT
License:	MIT
URL:		https://github.com/qarmin/czkawka
Source0:	https://github.com/qarmin/czkawka/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	vendor.tar.xz

BuildRequires:	rust-packaging
BuildRequires:	rust
BuildRequires:	rust-src
BuildRequires:	cargo
BuildRequires:	cargo-c
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pango)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gdk-3.0) >= 3.22
BuildRequires:	hicolor-icon-theme

%global srcroot %{_sourcedir}/%{pkgname}-%{version}

%description
Czkawka is simple, fast and easy to use alternative to Fslint, written in Rust.
This is my first ever project in Rust so probably a lot of things are not being written in the most optimal way.

%package -n %{pkgname}-%{cliapp}
Summary:	CLI frontend of Czkawka

%description -n %{pkgname}-%{cliapp}
CLI frontent of Czkawka.

%files -n %{pkgname}-%{cliapp}
%license LICENSE
%{_bindir}/%{pkgname}_%{cliapp}
%{_bindir}/%{pkgname}

%package -n %{pkgname}-%{guiapp}
Summary:	GTK frontend of Czkawka
Provides:	czkawka = %{version}-%{release}

%description -n %{pkgname}-%{guiapp}
GTK frontent of Czkawka.

%files -n %{pkgname}-%{guiapp}
%license LICENSE
%{_bindir}/%{pkgname}_%{guiapp}
%{_datadir}/applications/com.github.qarmin.czkawka.desktop
%{_iconsdir}/hicolor/scalable/apps/com.github.qarmin.czkawka.svg
%{_datadir}/metainfo/com.github.qarmin.czkawka.metainfo.xml

#package     -n %{pkgname}-%{orbapp}
#Summary:        Orbtk frontend of Czkawka

#description -n %{pkgname}-%{orbapp}
#Orbtk frontend of Czkawka

#files       -n %{pkgname}-%{orbapp}
#license LICENSE
#{_bindir}/%{pkgname}_%{guiapp}_%{orbapp}

%package -n %{pkgname}-doc
Summary:	Documentation of Czkawka
BuildArch:	noarch

%description -n %{pkgname}-doc
Documentation of Czkawka.

%files -n %{pkgname}-doc
%license LICENSE
%doc README.md
%doc Changelog.md

%prep
%autosetup -p1
tar -xf %{SOURCE1} -C %{_builddir}
%define cargo_registry %{_builddir}/vendor

%cargo_prep

%build
#cargo_build

cargo build --release --bin czkawka_gui
cargo build --release --bin czkawka_cli

%install
# Cargo install is broken. For some reason it not intall any files.
#cargo_install
mkdir -p %{buildroot}%{_bindir}/
install -Dm755 ./target/release/%{pkgname}_%{cliapp} %{buildroot}%{_bindir}
install -Dm755 ./target/release/%{pkgname}_%{guiapp} %{buildroot}%{_bindir}

ln -s %{_bindir}%{pkgname}_%{cliapp} %{buildroot}%{_bindir}/%{pkgname}

install -Dm644 ./data/icons/com.github.qarmin.czkawka.svg -t %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
install -Dm644 ./data/com.github.qarmin.czkawka.desktop -t %{buildroot}%{_datadir}/applications/
install -Dm644 ./data/com.github.qarmin.czkawka.metainfo.xml -t %{buildroot}%{_datadir}/metainfo

%if %{with check}
%check
%cargo_test
%endif
