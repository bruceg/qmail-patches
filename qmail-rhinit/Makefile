PREFIX = 
install = /usr/bin/install

mandir = /usr/man
bindir = /usr/bin
sharedir = /usr/share
svcdir = /var/qmail/service
etcdir = /etc
logdir = /var/log
profiledir = $(etcdir)/profile.d

all:

install:
	$(install) -d $(PREFIX)$(profiledir)
	$(install) -d $(PREFIX)$(bindir)
	$(install) -d $(PREFIX)$(sharedir)/qmail
	$(install) -d $(PREFIX)$(mandir)/man8
	$(install) profile.d/* $(PREFIX)$(profiledir)
	$(install) -m 644 share/* $(PREFIX)$(sharedir)/qmail
	$(install) -m 644 man8/* $(PREFIX)$(mandir)/man8
	$(install) bin/* $(PREFIX)$(bindir)
	for svc in svc/*-svc-run; do \
	  base=`basename $$svc -svc-run`; \
	  $(install) -d $(PREFIX)$(svcdir)/$$base; \
	  $(install) -m 755 $$svc $(PREFIX)$(svcdir)/$$base/run; \
	done
	for svc in svc/*-log-run; do \
	  base=`basename $$svc -log-run`; \
	  $(install) -d $(PREFIX)$(svcdir)/$$base/log; \
	  $(install) -m 755 $$svc $(PREFIX)$(svcdir)/$$base/log/run; \
	  chmod +t $(PREFIX)$(svcdir)/$$base; \
	  $(install) -d -m 700 $(PREFIX)$(logdir)/$$base; \
	done
