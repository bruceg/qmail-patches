[ -e /var/qmail/control/aliasempty ]
if ($status == 0) then
	set tmpmail=`sed -e '/^[^.]/d' -e "s|^|${HOME}/|" -e 's|/\./|/|g' /var/qmail/control/aliasempty | tail -1`
	if ("$tmpmail" != "") then
		setenv MAIL "$tmpmail"
	endif
	unset tmpmail
else
	setenv MAIL "${HOME}/Mailbox"
endif
setenv MAILDIR "$MAIL"
if ($?MANPATH) then
  setenv MANPATH "${MANPATH}:/var/qmail/man"
endif
