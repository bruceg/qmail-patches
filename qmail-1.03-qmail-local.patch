diff -u qmail-1.03.old/qmail-local.c qmail-1.03/qmail-local.c
--- qmail-1.03.old/qmail-local.c	1998-06-15 05:52:55.000000000 -0500
+++ qmail-1.03/qmail-local.c	2003-01-09 14:22:48.000000000 -0600
@@ -645,7 +645,7 @@
     {
      cmds.s[j] = 0;
      k = j;
-     while ((k > i) && (cmds.s[k - 1] == ' ') || (cmds.s[k - 1] == '\t'))
+     while ((k > i) && ((cmds.s[k - 1] == ' ') || (cmds.s[k - 1] == '\t')))
        cmds.s[--k] = 0;
      switch(cmds.s[i])
       {
