Name:		dmtcp
Version:	1.2.3
Release:	2.svn1321%{?dist}
Summary:	Checkpoint/Restart functionality for Linux processes
Group:		Applications/System
License:	LGPLv3+
URL:		http://dmtcp.sourceforge.net
# The source for this package was pulled from upstream's vcs. Use the following
# commands to generate the tarball:
#  svn export -r 1321 https://dmtcp.svn.sourceforge.net/svnroot/dmtcp/trunk dmtcp-1.2.3
#  fakeroot tar cf dmtcp-1.2.3+svn1321.tar dmtcp-1.2.3
#  gzip -9 dmtcp-1.2.3+svn1321.tar
Source0:	%{name}-%{version}+svn1321.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gcc-c++
BuildRequires:	gcc
BuildRequires:	glibc-devel
BuildRequires:	python

# This package is functional only on i386 and x86_64 architectures.
ExclusiveArch:	%ix86 x86_64

%description
DMTCP (Distributed MultiThreaded Checkpointing) is a tool to transparently
checkpointing the state of an arbitrary group of programs including
multi-threaded and distributed computations.  It operates directly on the user
binary executable, with no Linux kernel modules or other kernel mods.

Among the applications supported by DMTCP are OpenMPI, MATLAB, Python, Perl,
and many programming languages and shell scripting languages.  DMTCP also
supports GNU screen sessions, including vim/cscope and emacs. With the use of
TightVNC, it can also checkpoint and restart X-Windows applications, as long as
they do not use extensions (e.g.: no OpenGL, no video).

This package contains DMTCP binaries.

%package -n libdmtcpaware
Summary:	DMTCP programming interface
Group:		Development/Libraries
Requires:	%{name}%{?_isa}

%description -n libdmtcpaware
DMTCP (Distributed MultiThreaded Checkpointing) is a tool to transparently
checkpointing the state of an arbitrary group of programs including
multi-threaded and distributed computations.  It operates directly on the user
binary executable, with no Linux kernel modules or other kernel mods.

Among the applications supported by DMTCP are OpenMPI, MATLAB, Python, Perl,
and many programming languages and shell scripting languages.  DMTCP also
supports GNU screen sessions, including vim/cscope and emacs. With the use of
TightVNC, it can also checkpoint and restart X-Windows applications, as long as
they do not use extensions (e.g.: no OpenGL, no video).

This package provides a programming interface to allow checkpointed
applications to interact with dmtcp.

%package -n libdmtcpaware-devel
Summary:	DMTCP programming interface -- developer package
Group:		Development/Libraries
Requires:	libdmtcpaware%{?_isa} = %{version}

%description -n libdmtcpaware-devel
DMTCP (Distributed MultiThreaded Checkpointing) is a tool to transparently
checkpointing the state of an arbitrary group of programs including
multi-threaded and distributed computations.  It operates directly on the user
binary executable, with no Linux kernel modules or other kernel mods.

Among the applications supported by DMTCP are OpenMPI, MATLAB, Python, Perl,
and many programming languages and shell scripting languages.  DMTCP also
supports GNU screen sessions, including vim/cscope and emacs. With the use of
TightVNC, it can also checkpoint and restart X-Windows applications, as long as
they do not use extensions (e.g.: no OpenGL, no video).

This package provides libraries for developing applications that need to
interact with dmtcp.

%package -n libdmtcpaware-doc
Summary:	DMTCP programming interface -- basic examples
Group:		Development/Libraries
Requires:	libdmtcpaware-devel%{?_isa} = %{version}

%description -n libdmtcpaware-doc
This package provides some basic examples on how to use dmtcpaware.

%package -n libdmtcpaware-static
Summary:	DMTCP programming interface -- static library for devloper pkg
Group:		Development/Libraries
Requires:	libdmtcpaware-devel%{?_isa} = %{version}

%description -n libdmtcpaware-static
This package provides static library that can be used to bundle dmtcpaware code
with user application.

%prep
%setup -q

%build
sed -i -e 's/enable_option_checking=fatal/enable_option_checking=no/'\
  configure.ac
aclocal
autoconf --force
%configure --disable-option-checking
make %{?_smp_mflags}


%check
# disable the test for now as bash is failing with 32-bit when built on 64-bit machine.
#%%ifarch %%x86_64
#./test/autotest.py --slow
#%%endif

%install
make install DESTDIR=%{buildroot}
#%%make_install
#cp QUICK-START COPYING %%{buildroot}/%%{_defaultdocdir}/%%{name}-%%{version}/

%clean
rm -rf %{buildroot}

%post -n libdmtcpaware
/sbin/ldconfig

%postun -n libdmtcpaware
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/dmtcp_*
%{_bindir}/mtcp_restart
%{_libdir}/%{name}/dmtcphijack.so
%{_libdir}/%{name}/ptracehijack.so
%{_libdir}/%{name}/libmtcp.so
%doc QUICK-START COPYING
%{_docdir}/%{name}-%{version}/examples
%exclude %{_includedir}/mtcp.h
#%%{_defaultdocdir}/%%{name}-%%{version}/QUICK-START
#%%{_defaultdocdir}/%%{name}-%%{version}/COPYING
%{_mandir}/man1/dmtcp.1.gz
%{_mandir}/man1/dmtcp_*.1.gz
%{_mandir}/man1/mtcp.1.gz
%{_mandir}/man1/mtcp_restart.1.gz

%files -n libdmtcpaware
%defattr(-,root,root,-)
%{_libdir}/libdmtcpaware.so.*

%files -n libdmtcpaware-devel
%defattr(-,root,root,-)
%{_includedir}/dmtcpaware.h
%{_libdir}/libdmtcpaware.so

%files -n libdmtcpaware-doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/examples

%files -n libdmtcpaware-static
%defattr(-,root,root,-)
%{_libdir}/libdmtcpaware.a

%changelog
* Tue Oct 25 2011 kapil@ccs.neu.edu
- Updating to svn 1321.
- libdmtcpaware-devel-static renamed to libdmtcpaware-static
- %%{_isa} added to Requires
- disable_option_checking changed from "fatal" to "no"
- QUICK_START and COPYING installed using %%{doc}
* Mon Aug  9 2011 gene@ccs.neu.edu
- Updating to upstream release 1.2.3-1.svn1247M.
- svn revision 1246 adds objcopy to set section attribute in libmtcp.so
  (if debuginfo repo was present during build, limbtcp.so was missing a section)
- dmtcp.spec and 'make install' changed for improved file layout
* Tue Jul 26 2011 kapil@ccs.neu.edu
- Top level configure files updated to fix configure error.
* Fri Jul 22 2011 kapil@ccs.neu.edu
- Updating to upstream release 1.2.3.
* Sat Jul  2 2011 kapil@ccs.neu.edu
  * 1.2.2 release notes from upstream:
- A new module system, allowing users to write their own extensions to DMTCP,
  including wrappers around library calls. See the module subdirectory for
  examples.
- ./configure --enable-m32 was not working in DMTCP 1.2.1. It works again now.
- more bug fixes and robustness testing. Tested on kernels ranging from Linux
  2.6.5 to the latest kernel. Tested especially on the Linux distributions: Red
  Hat/Fedora, Debian/Ubuntu, SuSe/OpenSUSE; although we don't know of any Linux
  distributions where it fails to run.
- 'screen' did not checkpoint properly on machines using LDAP authentication.
  This could also affect processes using 'bash'. This has been fixed.
- Furthermore, recent versions of 'screen' began calling 'utempter' when
  present Support for 'utempter' and some other setuid processes has been
  added.
- Removed the requirement for libc.a in building DMTCP, since Red Hat does not
  include libc.a in its standard repository.
- ./configure --enable-ptrace now more robust. Still labelled "experimental"
  for this release. You will need to enable this if you want to checkpoint gdb
  sessions, programs running under strace, and certain other applications.
- ./configure --enable-fast-ckpt-restart can make ckpt/restart faster by using
  'mmap'. You will need to set the environment variable DMTCP_GZIP to "0" if
  you use this. This feature is still experimental, and there are many other
  tricks for speeding up ckpt/restart. Please talk to the developers if this is
  important for your application.
- Experimental support added for HBICT ( hbict.sf.net ). This provides support
  for incremental and differential checkpointing. However, this is still
  ongoing work.
- Work has begun on improved support for process migration between different
  Linux kernels and distributions. Simple applications should migrate. Please
  talk to us if this feature is important to you.
- We do not yet support the 'epoll' and 'inotify' Linux system calls. Recently,
  there has been some demand for this, and we intend to raise the priority.
  Please talk to us if this feature is important to you.
* Wed Jun 22 2011 kapil@ccs.neu.edu
- Exclude mtcp.c from installation.
* Wed Jun 22 2011 kapil@ccs.neu.edu
- Updating to upstream release 1.2.2.
* Fri Jun 17 2011 kapil@ccs.neu.edu
- libdmtcpaware.a moved to libdmtcpaware-devel-static package.
- dmtcpaware examples moved to libdmtcpaware-doc package.
* Fri Jun 10 2011 kapil@ccs.neu.edu
- Build requirements updated.
- Minor cleanup.
* Tue Jun  7 2011 kapil@ccs.neu.edu
- Added "ExclusiveArch %%ix86 x86_64" and removed ExcludeArch lines.
- buildroot not cleaned in %%install section.
* Sat May 14 2011 kapil@ccs.neu.edu
- dependency on libc.a removed for mtcp_restart.
- Several other bug fixes and improvements.
* Sat Mar 12 2011 kapil@ccs.neu.edu
- Updated to release 1.2.1
* Fri Mar 11 2011 kapil@ccs.neu.edu
- Remove debug flags.
* Fri Mar 11 2011 kapil@ccs.neu.edu
- Updated to revision 935.
* Thu Mar 10 2011 kapil@ccs.neu.edu
- Reverting tarball to prev version.
* Thu Mar 10 2011 kapil@ccs.neu.edu
- Testing fix for restart under 32-bit OSes.
* Thu Mar 10 2011 kapil@ccs.neu.edu
- Updated tarball with compiler warnings fixed.
* Thu Mar 10 2011 kapil@ccs.neu.edu
- Added python to dependency list for running make check.
* Thu Mar 10 2011 kapil@ccs.neu.edu
- Preparing for release 1.2.1. Pulled updates from the latest dmtcp svn.
