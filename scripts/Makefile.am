appletdir = $(libdir)/gnome-applets
applet_SCRIPTS = computertemp
applet_in_file = computertemp.in
$(applet_SCRIPTS): $(applet_in_file)
	sed -e "s|\@PYTHONDIR\@|$(pythondir)|" < $< > $@

DISTCLEANFILES = \
		$(applet_SCRIPTS)
		
EXTRA_DIST = \
		$(applet_in_file)
