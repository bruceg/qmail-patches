all: tars rpms

tars:
	tar -czf qmail-rhinit.tar.gz --exclude=CVS qmail-rhinit

rpms:
	su -c 'cp * /usr/src/redhat/SOURCES; cd /usr/src/redhat && nice rpm -ba --clean SOURCES/qmail-1.03+patches.spec && rm -f SOURCES/* && mv SRPMS/qmail-* RPMS/*/qmail-* ~-/RPMS && chown bruce.guenter ~-/RPMS/qmail-*.rpm'
	rpm --addsign RPMS/qmail-*.rpm
	#mv -v /tmp/qmail-*.rpm RPMS

RELEASE := $(shell perl -ne 'print if s/^Release:\s+//' qmail-1.03+patches.spec)
destdir=$(HOME)/websites/untroubled.org/www/qmail+patches
archdir=$(HOME)/archive/qmail+patches/

release-$(RELEASE).tar.gz: RPMS/qmail-1.03+patches-$(RELEASE).src.rpm
	mkdir $(RELEASE)
	cp *.html $(RELEASE)
	cd $(RELEASE) && \
	  rpm2cpio ../RPMS/qmail-1.03+patches-$(RELEASE).src.rpm | cpio -id && \
	  rm -f qmail-1.03.tar.gz && \
	  tar -czf ../release-$(RELEASE).tar.gz *
	rm -rf $(RELEASE)
	
install-archive: release-$(RELEASE).tar.gz
	ln RPMS/qmail-1.03+patches-$(RELEASE).src.rpm $(archdir)
	ln release-$(RELEASE).tar.gz $(archdir)
	chmod 444 $(archdir)/*

install-website:
	cp *.html $(destdir)
	rm -f $(destdir)/current/*
	ln $(archdir)/release-$(RELEASE).tar.gz \
	   $(archdir)/qmail-1.03+patches-$(RELEASE).src.rpm \
	   $(destdir)/current

install: install-archive install-website
