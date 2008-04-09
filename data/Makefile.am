serverdir       = $(libdir)/bonobo/servers
server_in_files = GNOME_ComputertempApplet.server.in
server_DATA     = $(server_in_files:.server.in=.server)
$(server_in_files): $(server_in_files:.server.in=.server.in.in)
	sed -e "s|\@LIBEXECDIR\@|$(libexecdir)|" $< > $@
@INTLTOOL_SERVER_RULE@

resourcesdir = $(datadir)/computertemp
resources_DATA = computertemp_menu.xml computertemp_menu2.xml

schemasdir = $(GCONF_SCHEMA_FILE_DIR)
schemas_in_files = computertemp.schemas.in
schemas_DATA = $(schemas_in_files:.schemas.in=.schemas)
@INTLTOOL_SCHEMAS_RULE@
                
if GCONF_SCHEMAS_INSTALL
install-data-local: install-schemas
install-schemas:
	GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) \
		$(GCONFTOOL) --makefile-install-rule $(schemas_DATA)
endif

CLEANFILES =			\
	$(server_in_files)	\
	$(server_DATA)		\
	$(schemas_DATA)

EXTRA_DIST =			\
	$(server_in_files)	\
	$(server_DATA)		\
	$(resources_DATA) 	\
	$(schemas_in_files)
