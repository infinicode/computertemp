AC_INIT(computertemp)

PACKAGE=computertemp
VERSION=0.9.6.1

AM_INIT_AUTOMAKE($PACKAGE, $VERSION)
AM_MAINTAINER_MODE

AM_PATH_PYTHON
PKG_CHECK_MODULES(PYGTK, pygtk-2.0)
AC_SUBST(PYGTK_CFLAGS)
AC_SUBST(PYGTK_LIBS)

AC_PROG_INTLTOOL([0.23])

GETTEXT_PACKAGE=$PACKAGE
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE")

ALL_LINGUAS="de en es fr it nl sv zh"
AM_GLIB_GNU_GETTEXT

PKG_CHECK_MODULES(GCONF, gconf-2.0)
AC_PATH_PROG(GCONFTOOL, gconftool-2)
AM_GCONF_SOURCE_2

appletdir=${prefix}/lib/gnome-applets
AC_SUBST(appletdir)

AC_OUTPUT([
Makefile
computertemp/Makefile
computertemp/computertemp_globals.py
scripts/Makefile
data/Makefile
data/computertemp.schemas
data/GNOME_ComputertempApplet.server.in
images/Makefile
po/Makefile.in
])
