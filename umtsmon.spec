%define name umtsmon
%define version 0.9
%define release %mkrel 1

Summary: Tool to control and monitor a wireless mobile network card
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.src.tar.gz
Patch0:	 umtsmon-0.8-fr_i18n.patch
License: GPLv2
Group: Communications
Url: https://umtsmon.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libusb-devel qt3-devel

%description
UMTSmon is a tool to control and monitor a wireless mobile network
card (GPRS, EDGE, WCDMA, UMTS, HSDPA). It handles PIN codes, operator
choice (roaming), signal strength and network statistics,
sending/receiving SMS.

%prep
%setup -q
%patch0 -p1 -b .fr_i18n
# do not use size-dependent icon path in desktop file
perl -pi -e 's/%{name}-128x128.png/%{name}.png/' %{name}.desktop

%build
%qmake_qt3
%make
%{qt3bin}/lrelease %{name}.pro

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -m755 %{name} %{buildroot}%{_bindir}/%{name}

install -d %{buildroot}%{_datadir}/applications
install -m644 %{name}.desktop %{buildroot}%{_datadir}/applications

install -d %{buildroot}%{_datadir}/%{name}/translations
install -m644 i18n/*.qm %{buildroot}%{_datadir}/%{name}/translations

install -d %{buildroot}%{_iconsdir}/hicolor/128x128/apps
install -m644 images/128/%{name}-128x128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%files
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/128x128/apps/%{name}.png
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/translations
%{_datadir}/%{name}/translations/%{name}_*.qm
