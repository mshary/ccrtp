# Copyright (C) 2014 David Sugar, Tycho Softworks.
# Copyright (C) 2015 Cherokees of Idaho.
#
# This file is free software; as a special exception the author gives
# unlimited permission to copy and/or distribute it, with or without
# modifications, as long as this notice is preserved.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, to the extent permitted by law; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.

%define libname libccrtp3

Summary:        A Common C++ Class Framework for RTP Packets
Name:           ccrtp
Version:        2.1.2
Release:        1
License:        SUSE-GPL-2.0+-with-openssl-exception
Group:          Development/Libraries/C and C++
URL:            http://www.gnu.org/software/ccrtp/
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  ucommon-devel >= 6.2.2
BuildRequires:  pkgconfig
BuildRequires:  gcc-c++
BuildRequires:  libgcrypt-devel
BuildRequires:  libtool
BuildRequires:  cmake

%description
GNU ccRTP is a generic, extensible and efficient C++ framework for
developing applications based on the Real-Time Transport Protocol
(RTP) from the IETF. It is based on Common C++ and provides a full
RTP/RTCP stack for sending and receiving of realtime data by the use
of send and receive packet queues. ccRTP supports unicast,
multi-unicast and multicast, manages multiple sources, handles RTCP
automatically, supports different threading models and is generic as
for underlying network and transport protocols.

%package -n %{libname}
Group: System/Libraries
Summary: Runtime library for GNU RTP Stack

%package devel
Group: Development/Libraries/C and C++
Summary: Headers and static link library for ccrtp
Requires: %{libname} = %{version}-%{release}
Requires: ucommon-devel >= 6.0.0
Requires: libgcrypt-devel
Provides: libccrtp-devel = %version
Obsoletes: libccrtp-devel < %version
Requires(post): info
Requires(preun): info

%description -n %{libname}
This package contains the runtime library needed by applications that use
the GNU RTP stack.

%description devel
This package provides the header files, link libraries, and
documentation for building applications that use GNU ccrtp.

%prep
%setup -q

%build
%cmake \
	-DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
    -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir}

%{__make} %{?_smp_mflags}

%install
%cmake_install

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README COPYING.addendum
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/ccrtp
%{_includedir}/ccrtp/*.h
%{_infodir}/ccrtp.info*

%post devel
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun devel
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%changelog
* Mon Mar 24 2014 David Sugar <dyfet@gnutelephony.org> - 2.0.7-0
- Initial osb build release - simpler than current one though

