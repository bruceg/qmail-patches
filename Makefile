RELEASE := $(shell perl -ne 'print if s/^Release:\s+//' qmail-1.03+patches.spec)
destdir = $(HOME)/websites/untroubled.org/www/qmail+patches
archdir = $(HOME)/archive/qmail+patches/$(RELEASE)
rpmsdir = $(PWD)/RPMS/$(RELEASE)
srpm = qmail-1.03+patches-$(RELEASE).src.rpm

all: tars rpms

tars: qmail-rhinit.tar.gz

qmail-rhinit.tar.gz: Makefile qmail-rhinit qmail-rhinit/* qmail-rhinit/*/*
	tar -czf qmail-rhinit.tar.gz --exclude=CVS qmail-rhinit

rpms: $(rpmsdir)/$(srpm)

$(rpmsdir)/$(srpm): $(rpmsdir) *
	su -c "cp * /usr/src/redhat/SOURCES; cd /usr/src/redhat && nice rpm -ba --clean SOURCES/qmail-1.03+patches.spec && rm -f SOURCES/* && mv SRPMS/qmail-* RPMS/*/qmail-* $(rpmsdir) && chown bruce.guenter $(rpmsdir)/qmail-*.rpm"
	rpm --addsign $(rpmsdir)/qmail-*.rpm

$(rpmsdir):
	mkdir -p $(rpmsdir)

install: install-archive install-website
	
install-archive: release-$(RELEASE).tar.gz
	mkdir -p $(archdir)
	ln $(rpmsdir)/$(srpm) $(archdir)
	ln release-$(RELEASE).tar.gz $(archdir)
	chmod 444 $(archdir)/*
	chmod 555 $(archdir)

install-website:
	cp *.html $(destdir)
	rm -f $(destdir)/current/*
	ln $(archdir)/release-$(RELEASE).tar.gz $(archdir)/$(srpm) \
	   $(destdir)/current

release-$(RELEASE).tar.gz: $(rpmsdir)/$(srpm)
	mkdir $(RELEASE)
	cp *.html $(RELEASE)
	cd $(RELEASE) && \
	  rpm2cpio ../$(rpmsdir)/$(srpm) | cpio -id && \
	  rm -f qmail-1.03.tar.gz && \
	  tar -czf ../release-$(RELEASE).tar.gz *
	rm -rf $(RELEASE)
