all: tars rpms

tars:
	tar -czf qmail-rhinit.tar.gz --exclude=CVS qmail-rhinit

rpms:
	su -c 'cp * /usr/src/redhat/SOURCES; cd /usr/src/redhat && rpm -ba SOURCES/qmail-1.03+patches.spec && rm -f SOURCES/* && mv SRPMS/qmail-* RPMS/*/qmail-* ~-/RPMS && chown bruce.guenter ~-/RPMS/qmail-*.rpm'
	#mv -v /tmp/qmail-*.rpm RPMS

RELEASE=16
destdir=$(HOME)/websites/em.ca/www/qmail+patches

install:
	mv $(destdir)/*.src.rpm $(destdir)/old
	cp *.html RPMS/*.src.rpm $(destdir)
	rm -f $(destdir)/sources/*
	cp cron.hourly dot.qmail-msglog *.patch *.spec *.sh \
		qmail-rhinit.tar.gz syncdir.c $(destdir)/sources
	cd $(destdir)/sources && tar -czf ../old/release-$(RELEASE).tar.gz *
