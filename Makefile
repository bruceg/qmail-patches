all: tars rpms

tars:
	tar -czf qmail-rhinit.tar.gz --exclude=CVS qmail-rhinit

rpms:
	su -c 'cp * /usr/src/redhat/SOURCES; cd /usr/src/redhat && rpm -ba SOURCES/qmail-1.03+patches.spec && rm -f SOURCES/* && mv SRPMS/qmail-* RPMS/*/qmail-* ~-/RPMS && chown bruce.guenter ~-/RPMS/qmail-*.rpm'
	#mv -v /tmp/qmail-*.rpm RPMS

RELEASE=18
destdir=$(HOME)/websites/em.ca/www/qmail+patches

HEADER.html: HEAD.html NEWS.html
	cat $^ >$@

install:
	cp *.html *.php* $(destdir)
	cp RPMS/qmail-1.03+patches-$(RELEASE).src.rpm $(destdir)/SRPMS
	tar -czf $(destdir)/sources/release-$(RELEASE).tar.gz \
		cron.hourly dot.qmail-msglog *.patch *.spec *.sh \
		qmail-rhinit.tar.gz syncdir.c
	rm -f $(destdir)/current/*
	ln $(destdir)/SRPMS/qmail-1.03+patches-$(RELEASE).src.rpm \
	   $(destdir)/sources/release-$(RELEASE).tar.gz \
	   $(destdir)/current
