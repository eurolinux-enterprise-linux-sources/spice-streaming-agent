Name:           spice-streaming-agent
Version:        0.2
Release:        3%{?dist}
Summary:        SPICE streaming agent
Group:          Applications/System
License:        ASL 2.0
URL:            https://www.redhat.com
Source0:        %{name}-%{version}.tar.xz

Patch1: 0001-start-streaming-check-num_codecs.patch
Patch2: 0002-LoadPlugin-call-dlclose-upon-failure.patch
Patch3: 0003-main-better-cleanup-when-XOpenDisplay-or-XFixesQuery.patch
Patch4: 0004-jpeg-Do-not-use-next_output_byte-buf_empty_output_bu.patch

BuildRequires:  spice-protocol >= 0.12.14
BuildRequires:  libX11-devel libXfixes-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  catch-devel
BuildRequires:  pkgconfig(udev)
# we need /usr/sbin/semanage program which is available on different
# packages depending on distribution
Requires(post): /usr/sbin/semanage
Requires(postun): /usr/sbin/semanage

ExclusiveArch: x86_64

%description
An agent, running on a guest, sending video streams of the X display to a
remote client (over SPICE).

%package devel
Requires: spice-protocol >= 0.12.14
Requires: pkgconfig
Summary:  SPICE streaming agent development files

%description devel
This package contains necessary header files to build SPICE streaming
agent plugins.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure --enable-tests --with-udevrulesdir=%{_udevrulesdir}
make %{?_smp_mflags} V=1

%check
make check

%install
make install DESTDIR=%{buildroot} V=1
if test -d "%{buildroot}/%{_libdir}/%{name}/plugins"; then
    find %{buildroot}/%{_libdir}/%{name}/plugins -name '*.la' -delete
fi

%post
semanage fcontext -a -t xserver_exec_t %{_bindir}/spice-streaming-agent 2>/dev/null || :
restorecon %{_bindir}/spice-streaming-agent || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t xserver_exec_t %{_bindir}/spice-streaming-agent 2>/dev/null || :
fi


%files
%doc COPYING NEWS README
%{_udevrulesdir}/90-spice-guest-streaming.rules
%{_bindir}/spice-streaming-agent
%{_sysconfdir}/xdg/autostart/spice-streaming.desktop
%{_datadir}/gdm/greeter/autostart/spice-streaming.desktop

%files devel
%defattr(-,root,root,-)
%{_includedir}
%{_libdir}/pkgconfig

%changelog
* Wed Aug  1 2018 Uri Lublin <uril@redhat.com> - 0.2-3
- Fix coverity issue
  Related: rhbz#1479294

* Wed Aug  1 2018 Uri Lublin <uril@redhat.com> - 0.2-2
- Fix coverity issues
- Fix mjpeg encoder
  Related: rhbz#1479294

* Thu May 31 2018 Uri Lublin <uril@redhat.com> - 0.2-1
- First release
  Related: rhbz#1479294

* Wed Aug 16 2017 Frediano Ziglio <fziglio@redhat.com> - 0.1-1
- Initial package (pre-release)
