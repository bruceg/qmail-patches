#!/bin/sh
client() {
	tcpclient -RHl0 -- "$1" 20025 sh -c 'exec grep -v "^  done	" <&6'
}
qs=/var/qmail/control/qmqpservers
if test -f $qs; then
	for server in `grep -v '^#' $qs | sort | uniq`
	do
		client $server
	done
else
	client 127.0.0.1
fi
