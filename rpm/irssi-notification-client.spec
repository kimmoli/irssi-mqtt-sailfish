#
# irssi-notification-client
#

%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Summary: irssi mqtt push notification client
Name: irssi-notification-client
Version: 1.0.2
Release: 2
License: LICENSE
Group: Utilities
Source0:    %{name}-%{version}.tar.bz2
BuildArch:  noarch
URL: https://wiki.merproject.org/wiki/Middleware/PushNotifications
Requires: python
Requires: python-mosquitto
Requires: dbus-python

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
%{summary}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}

# in builddir
cp -a * %{buildroot}
mv %{buildroot}/LICENSE %{buildroot}/usr/share/%{name}/
mv %{buildroot}/README.md %{buildroot}/usr/share/%{name}/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config /etc/systemd/user/%{name}.service
%config /usr/share/lipstick/notificationcategories/x-nemo.messaging.irssi.conf
/usr/share/%{name}/%{name}.py
/usr/share/%{name}/LICENSE
/usr/share/%{name}/README.md
/usr/share/%{name}/itsme.wav
/usr/share/%{name}

%post
systemctl-user start %{name}.service
systemctl-user enable %{name}.service


%pre
# In case of update, stop and disable first
if [ "$1" = "2" ]; then
  systemctl-user stop %{name}.service
  systemctl-user disable %{name}.service
fi

%preun
# in case of complete removal, stop and disable
if [ "$1" = "0" ]; then
  systemctl-user stop %{name}.service
  systemctl-user disable %{name}.service
fi
