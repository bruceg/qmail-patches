if [ -e /var/qmail/control/aliasempty ]; then
	tmpmail=`sed -e '/^\./!d' -e "s|^|${HOME}/|" -e 's|/\./|/|g' /var/qmail/control/aliasempty | tail -1`
	if [ -n "$tmpmail" ]; then MAIL="$tmpmail"; fi
	unset tmpmail
else
	MAIL=${HOME}/Mailbox
fi
MAILDROP="$MAIL"
export MAIL MAILDROP
