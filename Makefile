all: tars rpms

tars:
	tar -czf qmail-rhinit.tar.gz qmail-rhinit

rpms:
	su -c 'cp * /usr/src/redhat/SOURCES; cd /usr/src/redhat && rpm -ba SOURCES/qmail-1.03+patches.spec && rm -f SOURCES/* && mv SRPMS/qmail-* RPMS/*/qmail-* ~-/RPMS && chown bruce.guenter ~-/RPMS/qmail-*.rpm'
	#mv -v /tmp/qmail-*.rpm RPMS

