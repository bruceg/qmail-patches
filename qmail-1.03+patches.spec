Name: qmail
Version: 1.03+patches
Release: 16
Group: Networking/Daemons
URL: http://www.qmail.org/
Copyright: Check with djb@koobera.math.uic.edu
Packager: Bruce Guenter <bruceg@em.ca>
Source0: ftp://koobera.math.uic.edu/pub/software/qmail-1.03.tar.gz
Source1: qmail-rhinit.tar.gz
Source2: dot.qmail-msglog
Source3: syncdir.c
Source4: cron.hourly
Patch0: qmail-1.03-msglog.patch
Patch1: qmail-1.03-condredirect.patch
Patch2: qmail-1.03-showctl.patch
Patch3: qmail-1.03-bind-interface.patch
Patch4: http://www.qmail.org/big-todo.103.patch
Patch5: qmail-1.03-install-path-big-todo.patch
Patch6: qmail-1.03-autouidgid.patch
Patch7: qmail-1.03-syncdir.patch
Patch8: qmail-1.03-pop3d-stat.patch
Patch9: qmail-1.03-queuevar.patch
Patch10: qmail-1.03-big-dns.patch
Patch11: big-concurrency.patch
Summary: Qmail Mail Transfer Agent
Provides: MTA
Provides: smtpdaemon
Conflicts: sendmail
Conflicts: qmail-cyclog
Obsoletes: qmail-utils
BuildRoot: /tmp/qmail-root
Requires: chkconfig
Requires: initscripts
Requires: net-tools
Requires: sh-utils
Requires: shadow-utils
Requires: supervise-scripts >= 2.2

%description
Qmail is a small, fast, secure replacement for the sendmail package,
which is the program that actually receives, routes, and delivers
electronic mail.  *** Note: Be sure and read the documentation as there
are some small but very significant differences between sendmail and
qmail and the programs that interact with them.

The source for this RPM can be found at:
	http://em.ca/~bruceg/qmail+patches/

%package mailq
Group: Networking/Daemons
Summary: Support for the "mailq" command for qmail
Requires: qmail = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires: chkconfig
Requires: supervise-scripts >= 2.2
Requires: ucspi-unix
%description mailq
This package contains a local-domain daemon used to provide
non-privileged users access to the results from the mailq command.

%package pop3d
Group: Networking/Daemons
Summary: POP3 server support for qmail
Provides: pop3daemon
Requires: qmail = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires: chkconfig
Requires: sh-utils
Requires: supervise-scripts >= 2.2
Requires: ucspi-tcp >= 0.86-1
%description pop3d
Support files for running the qmail POP3 server.

%package qmtpd
Group: Networking/Daemons
Summary: QMTP server support for qmail
Provides: qmtpdaemon
Requires: qmail = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires: chkconfig
Requires: sh-utils
Requires: supervise-scripts >= 2.2
Requires: ucspi-tcp >= 0.86-1
%description qmtpd
Support files for running the qmail QMTP server.

%package smtpd
Group: Networking/Daemons
Summary: SMTP server support for qmail
Requires: qmail = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires: chkconfig
Requires: sh-utils
Requires: supervise-scripts >= 2.2
Requires: ucspi-tcp >= 0.86-1
%description smtpd
Support files for running the qmail SMTP server.
RBL blocking is supported by the rblsmtpd in the new ucspi-tcp package.

%package qmqpd
Group: Networking/Daemons
Summary: QMQP server support for qmail
Provides: qmqpdaemon
Requires: qmail = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires: chkconfig
Requires: sh-utils
Requires: supervise-scripts >= 2.2
Requires: ucspi-tcp >= 0.86-1
%description qmqpd
Support files for running the qmail QMQP server.

#%package spop3d
#Group: Networking/Daemons
#Summary: SSL-wrapped POP3 server support for qmail
#Provides: spop3daemon
#Requires: qmail = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
#Requires: chkconfig
#Requires: sh-utils
#Requires: supervise-scripts >= 2.2
#Requires: ucspi-tcp >= 0.86-1
#Requires: sslwrap
#%description spop3d
#Support files for running the qmail POP3 server with the SSL wrapper.

%prep
%setup -n qmail-1.03
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

fds=`ulimit -n`
let spawnlimit='(fds-6)/2'
echo $spawnlimit >conf-spawn

tar -xzf $RPM_SOURCE_DIR/qmail-rhinit.tar.gz

for source in cron.hourly dot.qmail-msglog syncdir.c; do
	cp $RPM_SOURCE_DIR/$source .
done

%build

make compile makelib
./compile syncdir.c
./makelib libsyncdir.a syncdir.o
make it man

pushd qmail-rhinit
  make "CFLAGS=$RPM_OPT_FLAGS" "LDFLAGS=-s" all
popd

%install
export PATH="/sbin:/usr/sbin:/bin:/usr/bin"
add_user() { useradd -d "$3" -g "$2" -M -r -s /bin/true "$1" || true; }
add_group() { groupadd -r "$1" || true; }
install_file() {
	source="$1"
	dest="$2"
	shift 2
	install "$@" "$source" $RPM_BUILD_ROOT/"$dest"
}

add_group qmail
add_group nofiles

add_user alias  nofiles /etc/qmail/alias
add_user qmaild nofiles /var/qmail
add_user qmaill nofiles /var/qmail
add_user qmailp nofiles /var/qmail
add_user qmailq qmail   /var/qmail
add_user qmailr qmail   /var/qmail
add_user qmails qmail   /var/qmail
add_user qmaillog qmail /var/log

/bin/rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}
install -d $RPM_BUILD_ROOT%{_sbindir}
pushd $RPM_BUILD_ROOT
  install -d etc/cron.hourly
  install -d -o alias -g qmail etc/qmail/alias
  install -d -o root -g qmail etc/qmail
  install -d -g qmail etc/qmail/control
  install -d -g qmail etc/qmail/owners
  install -d -g qmail etc/qmail/users
  install -d etc/tcpcontrol
  install -d usr/lib
  install -d -g qmail var/qmail
  #install -d -o qmaillog -g qmail var/log/{qmail,qmtpd,smtpd,pop3d,qmqpd}

  ln -s ../../etc/qmail/alias var/qmail/alias
  ln -s ../../etc/qmail/control var/qmail/control
  ln -s ../../etc/qmail/owners var/qmail/owners
  ln -s ../../etc/qmail/users var/qmail/users
  ln -s ../..%{_bindir} var/qmail/bin
  ln -s ../..%{_mandir} var/qmail/man
popd

# Build the user and group files, required for qmail-hier
./make-owners .
# INSTALL IT
./install $RPM_BUILD_ROOT/var/qmail
# CHECK IT
./instcheck $RPM_BUILD_ROOT/var/qmail

# Remove preformatted man pages
rm -rf $RPM_BUILD_ROOT/var/qmail/man/cat*
rm $RPM_BUILD_ROOT/var/qmail/man

# Fix for sendmail add-ons
pushd $RPM_BUILD_ROOT/usr
  mv bin/sendmail sbin/sendmail
  ln -s ../sbin/sendmail lib/sendmail
popd

# Install some extra configuration programs
install ipmeprint $RPM_BUILD_ROOT%{_bindir}

pushd qmail-rhinit
  make PREFIX=$RPM_BUILD_ROOT bindir=%{_bindir} mandir=%{_mandir} install
popd

# Install extra shell scripts
install_file cron.hourly etc/cron.hourly/qmail -m 755

install_file dot.qmail-msglog etc/qmail/alias/.qmail-msglog

pushd $RPM_BUILD_ROOT/etc/qmail/alias
  echo '&root' >.qmail-postmaster
  echo '&root' >.qmail-mailer-daemon
  touch .qmail-root
  chmod 644 .qmail*
popd

pushd $RPM_BUILD_ROOT/etc/qmail/control
  touch defaultdomain locals me plusdomain rcpthosts
  chmod 644 defaultdomain locals me plusdomain rcpthosts
popd

pushd $RPM_BUILD_ROOT/etc/qmail/users
  touch append assign cdb include exclude mailnames subusers
  chmod 644 *
popd

$RPM_BUILD_ROOT%{_bindir}/make-owners $RPM_BUILD_ROOT/etc/qmail

echo ./Maildir/ >$RPM_BUILD_ROOT/etc/qmail/control/aliasempty

# rebuild the sym-links under /var/qmail
pushd $RPM_BUILD_ROOT/var/qmail
  rm -f alias control users owners bin man
  ln -s /etc/qmail/alias alias
  ln -s /etc/qmail/control control
  ln -s /etc/qmail/owners owners
  ln -s /etc/qmail/users users
  ln -s %{_bindir} bin
  ln -s %{_mandir} man
  rm -rf boot
  rm -rf doc
  ln -s %{_docdir}/qmail-$RPM_PACKAGE_VERSION doc
popd

# Build the default tcpcontrol rules & CDBs
pushd $RPM_BUILD_ROOT/etc/tcpcontrol
  echo :allow >pop-3.rules
  echo :deny >qmqp.rules
  echo :allow >qmtp.rules
  #echo :allow >spop3.rules
  echo :allow >smtp.rules
  tcprules pop-3.cdb pop-3.tmp <pop-3.rules
  tcprules qmqp.cdb qmqp.tmp <qmqp.rules
  tcprules qmtp.cdb qmtp.tmp <qmtp.rules
  #tcprules spop3.cdb spop3.tmp <spop3.rules
  tcprules smtp.cdb smtp.tmp <smtp.rules
popd

%clean
rm -rf $RPM_BUILD_ROOT

# Pre/Post-install Scripts #####################################################
%pre
PATH="/sbin:/usr/sbin:$PATH" export PATH
add_user() { grep "^$1:" /etc/passwd >/dev/null || useradd -d "$3" -g "$2" -M -r -s /bin/true "$1"; }
add_group() { grep "^$1:" /etc/group >/dev/null || groupadd -r "$1"; }

if [ $1 = 2 ]; then
	# Disable deliveries if upgrading
	test -d /etc/qmail/alias && chmod +t /etc/qmail/alias
	test -d /var/qmail/alias && chmod +t /var/qmail/alias
	test -d /home && chmod +t /home/*
fi

add_group qmail
add_group nofiles

add_user alias  nofiles /etc/qmail/alias
add_user qmaild nofiles /var/qmail
add_user qmaill nofiles /var/qmail
add_user qmailp nofiles /var/qmail
add_user qmailq   qmail /var/qmail
add_user qmailr   qmail /var/qmail
add_user qmails   qmail /var/qmail
add_user qmaillog qmail /var/log

%post
if [ $1 = 2 ]; then
  # Re-enable deliveries on upgrading
  test -d /etc/qmail/alias && chmod -t /etc/qmail/alias
  test -d /var/qmail/alias && chmod -t /var/qmail/alias
  test -d /home && chmod -t /home/*
fi
%{_bindir}/qmail-rhconfig
%{_bindir}/make-owners /etc/qmail
/sbin/chkconfig --add qmail
/sbin/chkconfig --add qread
/sbin/chkconfig --add qstat

%post pop3d
/sbin/chkconfig --add pop3d

%post qmqpd
/sbin/chkconfig --add qmqpd

%post qmtpd
/sbin/chkconfig --add qmtpd

%post smtpd
/sbin/chkconfig --add smtpd
if [ "$1" = 1 ]; then
  cd /etc
  if [ -f inetd.conf ]; then
    if ! [ -e inetd.conf.rpmsave ]; then
      cp inetd.conf inetd.conf.rpmsave
    fi
    sed	-e 's/^smtp[ 	]/#smtp	/' inetd.conf >inetd.conf.new
    mv inetd.conf.new inetd.conf
    echo "inetd may need to be restarted before incoming SMTP connections"
    echo "will work.  Do this by typing '/etc/rc.d/init.d/inet restart'"
  fi
fi

%preun
if [ $1 -gt 0 ]; then exit 0; fi

test -x /etc/rc.d/init.d/qmail && /etc/rc.d/init.d/qmail stop

/sbin/chkconfig --del qmail
echo "Removing Qmail user ids..."
userdel alias
userdel qmaild
userdel qmaill
userdel qmailp
userdel qmailq
userdel qmailr
userdel qmails
userdel qmaillog

echo "Removing Qmail group ids..."
groupdel qmail
groupdel nofiles

%preun pop3d
if [ $1 -gt 0 ]; then exit 0; fi
test -x /etc/rc.d/init.d/pop3d && /etc/rc.d/init.d/pop3d stop
/sbin/chkconfig --del pop3d

%preun qmqpd
if [ $1 -gt 0 ]; then exit 0; fi
test -x /etc/rc.d/init.d/qmqpd && /etc/rc.d/init.d/qmqpd stop
/sbin/chkconfig --del qmqpd

%preun qmtpd
if [ $1 -gt 0 ]; then exit 0; fi
test -x /etc/rc.d/init.d/qmtpd && /etc/rc.d/init.d/qmtpd stop
/sbin/chkconfig --del qmtpd

%preun smtpd
if [ $1 -gt 0 ]; then exit 0; fi
test -x /etc/rc.d/init.d/smtpd && /etc/rc.d/init.d/smtpd stop
/sbin/chkconfig --del smtpd

# Files List ###################################################################
%files
%defattr(-,root,qmail)
%config /etc/profile.d/*

%defattr(-,-,qmail)
%config /etc/cron.hourly/qmail
%dir /etc/qmail

%attr(2755, alias, qmail) %dir /etc/qmail/alias/
%attr(-, alias, qmail) %config(noreplace) /etc/qmail/alias/.qmail-*

%dir /etc/qmail/owners
%config /etc/qmail/owners/*

%dir /etc/qmail/users
%ghost %config(missingok,noreplace) /etc/qmail/users/assign
%ghost %config(missingok,noreplace) /etc/qmail/users/cdb
%ghost %config(missingok,noreplace) /etc/qmail/users/include
%config(noreplace) /etc/qmail/users/append
%config(noreplace) /etc/qmail/users/exclude
%config(noreplace) /etc/qmail/users/mailnames
%config(noreplace) /etc/qmail/users/subusers

%dir /etc/qmail/control
%ghost %config(missingok,noreplace) /etc/qmail/control/defaultdomain
%ghost %config(missingok,noreplace) /etc/qmail/control/locals
%ghost %config(missingok,noreplace) /etc/qmail/control/plusdomain
%ghost %config(missingok,noreplace) /etc/qmail/control/rcpthosts
%verify(mode,group,user) %config(noreplace) /etc/qmail/control/aliasempty
%verify(mode,group,user) %config(noreplace) /etc/qmail/control/me

/etc/rc.d/init.d/qmail
/etc/rc.d/init.d/qread
/etc/rc.d/init.d/qstat

%attr(-,root,qmail) %doc BLURB BLURB2 BLURB3 BLURB4 CHANGES FAQ FILES
%attr(-,root,qmail) %doc INSTALL INSTALL.* INTERNALS PIC.* README REMOVE.*
%attr(-,root,qmail) %doc SECURITY SENDMAIL TEST.* THANKS THOUGHTS TODO UPGRADE

%{_bindir}/bouncesaying
%{_bindir}/condredirect
%{_bindir}/datemail
%{_bindir}/elq
%{_bindir}/except
%{_bindir}/forward
%{_bindir}/ipmeprint
%{_bindir}/maildir2mbox
%{_bindir}/maildirmake
%{_bindir}/maildirwatch
%{_bindir}/mailsubj
%{_bindir}/make-owners
%{_bindir}/pinq
%{_bindir}/predate
%{_bindir}/preline
%{_bindir}/qail
%{_bindir}/qbiff
%attr(0711,root,qmail) %{_bindir}/qmail-clean
%attr(0711,root,qmail) %{_bindir}/qmail-getpw
%{_bindir}/qmail-inject
%attr(0711,root,qmail) %{_bindir}/qmail-local
%attr(0700,root,qmail) %{_bindir}/qmail-lspawn
%attr(0700,root,qmail) %{_bindir}/qmail-newmrh
%attr(0700,root,qmail) %{_bindir}/qmail-newu
%{_bindir}/qmail-pop3d
%attr(0700,root,qmail) %{_bindir}/qmail-popup
%attr(0711,root,qmail) %{_bindir}/qmail-pw2u
%{_bindir}/qmail-qmqpc
%{_bindir}/qmail-qmqpd
%{_bindir}/qmail-qmtpd
%{_bindir}/qmail-qread
%{_bindir}/qmail-qstat
%attr(04711,qmailq,qmail) %{_bindir}/qmail-queue
%attr(0711,root,qmail) %{_bindir}/qmail-remote
%{_bindir}/qmail-rhconfig
%attr(0711,root,qmail) %{_bindir}/qmail-rspawn
%attr(0711,root,qmail) %{_bindir}/qmail-send
%{_bindir}/qmail-showctl
%{_bindir}/qmail-smtpd
%attr(0700,root,qmail) %{_bindir}/qmail-start
%{_bindir}/qmail-tcpok
%{_bindir}/qmail-tcpto
%{_bindir}/qreceipt
%{_bindir}/qsmhook
%attr(0711,root,qmail) %{_bindir}/splogger
%{_bindir}/tcp-env

/usr/lib/sendmail

%{_mandir}/man?/*

/usr/share/qmail

%{_sbindir}/sendmail

%attr(1755,root,qmail) %dir /var/service/qmail
%dir /var/service/qmail/log
%config /var/service/qmail/log/run
%config /var/service/qmail/run

/var/qmail

%files mailq
%defattr(-,root,qmail)
%{_bindir}/mailq
%dir /var/service/qread
%config /var/service/qread/run
%dir /var/service/qstat
%config /var/service/qstat/run

%files pop3d
%defattr(-,root,qmail)
/etc/rc.d/init.d/pop3d
%config(noreplace) /etc/tcpcontrol/pop-3.cdb
%config(noreplace) /etc/tcpcontrol/pop-3.rules
%attr(1755,root,qmail) %dir /var/service/pop3d
%dir /var/service/pop3d/log
%config /var/service/pop3d/log/run
%config /var/service/pop3d/run

%files qmqpd
%defattr(-,root,qmail)
/etc/rc.d/init.d/qmqpd
%config(noreplace) /etc/tcpcontrol/qmqp.cdb
%config(noreplace) /etc/tcpcontrol/qmqp.rules
%attr(1755,root,qmail) %dir /var/service/qmqpd
%dir /var/service/qmqpd/log
%config /var/service/qmqpd/log/run
%config /var/service/qmqpd/run

%files qmtpd
%defattr(-,root,qmail)
/etc/rc.d/init.d/qmtpd
%config(noreplace) /etc/tcpcontrol/qmtp.cdb
%config(noreplace) /etc/tcpcontrol/qmtp.rules
%attr(1755,root,qmail) %dir /var/service/qmtpd
%dir /var/service/qmtpd/log
%config /var/service/qmtpd/log/run
%config /var/service/qmtpd/run

%files smtpd
%defattr(-,root,qmail)
/etc/rc.d/init.d/smtpd
%config(noreplace) /etc/tcpcontrol/smtp.cdb
%config(noreplace) /etc/tcpcontrol/smtp.rules
%attr(1755,root,qmail) %dir /var/service/smtpd
%dir /var/service/smtpd/log
%config /var/service/smtpd/log/run
%config /var/service/smtpd/run

#%files spop3d
#%defattr(-,root,qmail)
#/etc/rc.d/init.d/pop3d
#%config(noreplace) /etc/tcpcontrol/spop3.cdb
#%config(noreplace) /etc/tcpcontrol/spop3.rules
#%attr(1755,root,qmail) %dir /var/service/spop3d
#%dir /var/service/spop3d/log
#%config /var/service/spop3d/log/run
#%config /var/service/spop3d/run

