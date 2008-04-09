# -*- coding: UTF-8 -*-

# +-------------------------------------------------------------------------------------+
# | GPL											|
# +-------------------------------------------------------------------------------------+
# | Copyright (c) 2005,2006 Adolfo González Blázquez <code@infinicode.org>		|
# |											|
# | This program is free software; you can redistribute it and/or			|
# | modify it under the terms of the GNU General Public License				|
# | as published by the Free Software Foundation; either version 2			|
# | of the License, or (at your option) any later version.				|
# |											|
# | This program is distributed in the hope that it will be useful,			|
# | but WITHOUT ANY WARRANTY; without even the implied warranty of			|
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the			|
# | GNU General Public License for more details.					|
# |											|
# | You should have received a copy of the GNU General Public License			|
# | along with this program; if not, write to the Free Software				|
# | Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.	|
# +-------------------------------------------------------------------------------------+


import pygtk
pygtk.require('2.0')
import gtk
import gobject
import gnome
import gnomeapplet

import time
import sys
import os
import string
import gc

# Import libraries
try:
	import computertemp
	from computertemp import temp_meta as tempf
	from computertemp import computertemp_globals as glob
	from computertemp import computertemp_prefs as prefs
	from computertemp import computertemp_gconf as gconf
except ImportError:
	print "Error importing computertemp libs"
	sys.exit()
	
# Internationalize
import locale
import gettext

gettext.bindtextdomain('computertemp', '/usr/share/locale')
gettext.textdomain('computertemp')
locale.bindtextdomain('computertemp', '/usr/share/locale')
locale.textdomain('computertemp')
gettext.install('computertemp', '/usr/share/locale', unicode=1)

	
# Main Class
class computertempApplet(gnomeapplet.Applet):
  
	# Set files and dir logs
	def setlogfilename(self):
		
		if self.autologname or self.log_filename == '':
			self.log_filename = self.log_filename_default
		self.gconf.save_prefs_log_filename()

			
	def setloginfo(self):
		
		if self.log_info == '':
			self.log_info = self.log_info_default
		self.gconf.save_prefs_log_info()
			
			
	def init_log_tooltips(self):
		
		self.tips_logname = \
			"Possible substitution patterns: \n" + \
			"{home}		/home/user \n" + \
			"{date}		22feb1980 \n" + \
			"{year}		1980 \n" + \
			"{month}		02 \n" + \
			"{monthname}	february \n" + \
			"{monthsimp}	feb \n" +\
			"{day}		22 \n" +\
			"{dayname}	friday \n" + \
			"{daysimp}	fri \n" + \
			"{applet}		applet_2 \n" + \
			"{sensor}		HHDTEMP "
			
		self.tips_loginfo = \
			"Possible substitution patterns: \n" + \
			"{temp}		46 \n" + \
			"{unit}		°C or °F \n" + \
			"{applet}		applet_2 \n" + \
			"{sensor}		HHDTEMP \n" + \
			"{zone}		TZ1 \n" + \
			"\n" + \
			"{compdate}	Fri Feb  22 23:12:02 1980 \n" + \
			"{date}		22feb1980 \n" + \
			"{time}		23:12:02 \n" + \
			"{year}		1980 \n" + \
			"{month}		02 \n" + \
			"{monthname}	february \n" + \
			"{monthsimp}	feb \n" +\
			"{day}		22 \n" +\
			"{dayname}	friday \n" + \
			"{daysimp}	fri \n" + \
			"\n" + \
			"{user}		username \n" + \
			"{sysname}	Linux \n" + \
			"{hostname}	localhost \n" + \
			"{kernel}		2.6.15-27-686 \n" + \
			"{arch}		i686 \n" + \
			"\n" + \
			"#			tabulator "
			
			
	# Changes logfilename if special patterns found on preferences dialog
	def parselogfilename(self, logname):
		
		logname = logname.replace('{home}', os.environ["HOME"])
		logname = logname.replace('{date}', time.strftime("%d%b%Y", time.localtime()))
		logname = logname.replace('{year}', time.strftime("%Y", time.localtime()))
		logname = logname.replace('{month}', time.strftime("%m", time.localtime()))
		logname = logname.replace('{monthname}', time.strftime("%B", time.localtime()))
		logname = logname.replace('{monthsimp}', time.strftime("%b", time.localtime()))
		logname = logname.replace('{day}', time.strftime("%d", time.localtime()))
		logname = logname.replace('{dayname}', time.strftime("%A", time.localtime()))
		logname = logname.replace('{daysimp}', time.strftime("%a", time.localtime()))
		logname = logname.replace('{applet}', self.gconf.get_applet_name())
		logname = logname.replace('{sensor}', self.tempmon.get_sensor_name()).replace(' ','_')
		return logname

	
	def parseloginfo(self, loginfo):

		if self.visualization_units == 1: unit = "°F"
		else: unit = "°C"
		
		loginfo = loginfo.replace('{temp}', `int(self.data)`)
		loginfo = loginfo.replace('{unit}', unit)
		loginfo = loginfo.replace('{applet}', self.gconf.get_applet_name())
		loginfo = loginfo.replace('{sensor}', self.tempmon.get_sensor_name())
		loginfo = loginfo.replace('{zone}', self.tempmon.get_zone_display_name(self.thermalzone))
		loginfo = loginfo.replace('{compdate}', time.asctime(time.localtime()))
		loginfo = loginfo.replace('{date}', time.strftime("%d%b%Y", time.localtime()))
		loginfo = loginfo.replace('{time}', time.strftime("%H:%M:%S", time.localtime()))
		loginfo = loginfo.replace('{year}', time.strftime("%Y", time.localtime()))
		loginfo = loginfo.replace('{month}', time.strftime("%m", time.localtime()))
		loginfo = loginfo.replace('{monthname}', time.strftime("%B", time.localtime()))
		loginfo = loginfo.replace('{monthsimp}', time.strftime("%b", time.localtime()))
		loginfo = loginfo.replace('{day}', time.strftime("%d", time.localtime()))
		loginfo = loginfo.replace('{dayname}', time.strftime("%A", time.localtime()))
		loginfo = loginfo.replace('{daysimp}', time.strftime("%a", time.localtime()))
		loginfo = loginfo.replace('{user}', os.environ["USER"])
		loginfo = loginfo.replace('{sysname}', os.uname()[0])
		loginfo = loginfo.replace('{hostname}', os.uname()[1])
		loginfo = loginfo.replace('{kernel}', os.uname()[2])
		loginfo = loginfo.replace('{arch}', os.uname()[4])
		loginfo = loginfo.replace('#', '\t')
		return loginfo
	

	# Calculates temperature depending on preferences (celsius or fahrenheit)
	def temperature(self, temp):
		if self.visualization_units == 1:
			return int(round(long(temp) * 9.00/5.00 + 32.00))
		else: return temp

	
	# Display dialog window error
	def dialog(self, text):
		dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
		dialog.run()
		dialog.destroy()
		
		
	def set_icon(self, path):
		self.icon.clear()
		gc.collect()
		self.icon.set_from_file(self.icon_path)
			
			
	# Update applet icon depending on temperature
	def update_icon(self):
	
		if self.visualization_mode == 1: self.icon.hide()
		else:
			self.icon.show()
			
			if self.tempmon.get_sensor_name() == "HDDTEMP":
				prefix = "hd"
			else:
				prefix = "temp"
				
			if self.tempmon_enabled:
				diff = (self.max_temp - self.min_temp) / 4
	
				temp = self.temperature(int(self.tempmon.get_zone_temp(self.tempmon.get_zone_name(self.thermalzone))))
		
				if temp < self.min_temp+(diff*1) and self.tempzone != 1:
					self.tempzone = 1
					self.icon_path = glob.pixmaps_dir + "/" + prefix + "_25.png"
					self.set_icon(self.icon_path)
				elif self.min_temp+(diff*1) <= temp < self.min_temp+(diff*2) and self.tempzone != 2:
					self.icon_path = glob.pixmaps_dir + "/" + prefix + "_50.png"
					self.tempzone = 2
					self.set_icon(self.icon_path)
				elif self.min_temp+(diff*2) <= temp < self.min_temp+(diff*3) and self.tempzone != 3:
					self.icon_path = glob.pixmaps_dir + "/" + prefix + "_75.png"
					self.tempzone = 3
					self.set_icon(self.icon_path)
				elif self.min_temp+(diff*3) <= temp and self.tempzone != 4:
					self.icon_path = glob.pixmaps_dir + "/" + prefix + "_100.png"
					self.tempzone = 4
					self.set_icon(self.icon_path)
			else:
				self.icon_path = glob.pixmaps_dir + "/temp_na.png"
				self.tempzone = 0
				self.set_icon(self.icon_path)
			
					
	# Updates data shown on applet tooltip
	def update_tooltip(self):
	
		if self.tempmon_enabled:
			text = _(' Temperatures ')

			if self.visualization_units == 1: unit = "°F"
			else: unit = "°C"
			
			count = 0
			for i in xrange(len(self.thermal_zones)):
				text += "\n   %s: %s%s" % \
					(self.tempmon.get_zone_display_name(i),
					 int(self.temperature (self.tempmon.get_zone_temp(self.thermal_zones[i]))), unit)
				if count == self.thermalzone: text += " *"
				count += 1
			
			# Debug info on tooltip and console
			if self.debug:
				diff = (self.max_temp - self.min_temp) / 4
				zones =  `self.min_temp` + ' - ' + `self.min_temp+(diff*1)` + ' - ' + `self.min_temp+(diff*2)`+ ' - ' + `self.min_temp+(diff*3)`
				text += "\n\n Debug"
				text += "\n   Applet name: %s" % self.gconf.get_applet_name()
				text += "\n   Sensor: %s" % self.tempmon.get_sensor_name()
				text += "\n   Enabled: %s" % self.tempmon_enabled
				text += "\n   Logging: %s" % self.logging
				text += "\n   Alarm: %s" % self.alarm_enabled
				text += "\n   Min Temp: %s" % self.min_temp
				text += "\n   Max Temp: %s" % self.max_temp
				text += "\n   Zone: %s     (%s)" % (self.tempzone, zones)
				text += "\n   Temp timeout: %s" % (self.timeout / 1000)
				text += "\n   Log timeout: %s" % (self.timeout_log / 1000)
				text += "\n   GConf key: %s" % self.gconf.gconf_applet
				text += "\n   Icon: %s" % self.icon_path
				text += "\n   Log: %s" % self.parselogfilename(self.log_filename)
			
			self.tooltip.set_tip(self.applet, text)
		else:
			self.tooltip.set_tip(self.applet, _('No Thermal Monitor Support!'))
			
	# Update text
	def update_text(self):
	
		if self.visualization_mode == 0:
			self.temp.hide()
		else:
			self.temp.show()

			if self.tempmon_enabled:
				self.data = int(self.tempmon.get_zone_temp(self.tempmon.get_zone_name(self.thermalzone)))

				if self.visualization_units == 1: unit = "°F"
				else: unit = "°C"
			
				self.temp.set_text(`self.temperature(self.data)`+unit)
			else:
				self.temp.set_text(self.data)
	
	
	# Logging
	def update_log(self):
	
		if self.logging:
			
			log_filename = self.parselogfilename(self.log_filename)
			log_info = self.parseloginfo(self.log_info)
			
			if not os.path.isdir(os.path.dirname(log_filename)):
				try:
					os.mkdir(os.path.dirname(log_filename))
				except OSError:
					print _('There was an error creating directory'), os.path.dirname(log_filename)
					self.dialog(_('Can not create directory \'%s\'\nPlease select another path') % os.path.dirname(log_filename))
					self.log_filename = self.log_filename_default
					self.setlogfilename()
					self.prefs.logentry.set_text(self.log_filename)
					self.prefs.logcheck.set_active(False)
					self.autologcheck = True
					self.autologname = True
					#self.prefs.logentry.set_sensitive(True)
					self.logging = False
					self.prefs.logentry.set_sensitive(False)
					self.prefs.preferences_show(None)
			else:
				try:
					file = open(log_filename, "a")
					file.write(log_info)
					if self.alarm_running: file.write("\tALARM!")
					file.write('\n')
					file.close()
				except IOError:
					print _('There was an error writing to'), log_filename
					self.dialog(_('Can not write to \'%s\'\nPlease select another path') % log_filename)
					self.log_filename = self.log_filename_default
					self.setlogfilename()
					self.prefs.logentry.set_text(self.log_filename)
					self.prefs.logcheck.set_active(False)
					self.logging = False
					self.prefs.logentry.set_sensitive(False)
					self.prefs.preferences_show(None)
				
				
	def update_alarm(self):
		
		# Is the command still being executed?
		try:
			self.alarm_alive = not os.waitpid(self.alarm_pid, os.WNOHANG)[0]
		except OSError:
			self.alarm_alive = False
		
		if self.alarm_enabled:
			
			if not self.alarm_running: # alarm_running = False
				
				if self.alarm_when:
					if self.data > self.alarm_limit:
						self.alarm_running = True
						commands = self.alarm_command.split(' ')
						self.alarm_pid = os.spawnvpe(os.P_NOWAIT, commands[0], commands, os.environ)
				else:
					if self.data < self.alarm_limit:
						self.alarm_running = True
						commands = self.alarm_command.split(' ')
						self.alarm_pid = os.spawnvpe(os.P_NOWAIT, commands[0], commands, os.environ)
						
			else: # alarm_running = True
				
				if self.alarm_repeat and not self.alarm_alive:
					commands = self.alarm_command.split(' ')
					self.alarm_pid = os.spawnvpe(os.P_NOWAIT, commands[0], commands, os.environ)
					
				if self.alarm_when:
					if self.data < self.alarm_limit: self.alarm_running = False
				else:
					if self.data > self.alarm_limit: self.alarm_running = False

				
	# Reset the alarm if the command is not being executed
	def reset_alarm(self):
		self.alarm_running = False or self.alarm_alive
				

	# Update data displayed on icon
	def update_temp(self):

		self.update_icon()
		self.update_text()
		self.update_tooltip()
		self.update_alarm()


	def update_main(self):
		
		# Update log if necessary
		if self.timeout_log_count % (self.timeout_log / 1000) == 0:
			self.timeout_log_count = 0
			self.update_log()
		self.timeout_log_count += 1
		
		# Update temperatures (icon, text and tooltips) if necessary
		if self.timeout_count % (self.timeout / 1000) == 0:
			self.timeout_count = 0
			self.update_temp()
		self.timeout_count += 1

		return True


	# Callback: panel background changed
	def change_background(self, panelapplet, backgroundtype, color, pixmap):
		self.applet.modify_bg(gtk.STATE_NORMAL, color)
		self.box.modify_bg(gtk.STATE_NORMAL, color)
		
		if pixmap is not None:
			s1 = self.applet.get_style()
			s2 = self.box.get_style()
			s1.bg_pixmap[gtk.STATE_NORMAL] = pixmap
			s2.bg_pixmap[gtk.STATE_NORMAL] = pixmap


	# Callback: panel orientation changed
	def change_orientation(self,arg1,data):
			self.orientation = self.applet.get_orient()

			self.inside_applet.remove(self.icon)
			self.inside_applet.remove(self.temp)
			self.box.remove(self.inside_applet)
			
			if self.orientation == 2 or self.orientation == 3:
				self.inside_applet = gtk.VBox()
			else:
				self.inside_applet = gtk.HBox()
				
			self.inside_applet.pack_start(self.icon)
			self.inside_applet.pack_start(self.temp)
			self.inside_applet.show_all()
			self.box.add(self.inside_applet)

	# Draws applet
	def create_applet(self):
		
		app_window = self.applet
		
		# Creates eventbox
		event_box = gtk.EventBox()
		event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK | 
			gtk.gdk.POINTER_MOTION_MASK | 
			gtk.gdk.POINTER_MOTION_HINT_MASK |
			gtk.gdk.CONFIGURE )
		
		# Creates icon for applet
		self.icon = gtk.Image()
		self.update_icon()
		
		# Create label for temp
		self.temp = gtk.Label()
		self.update_text()
		
		# Creates hbox with icon and temp
		self.inside_applet = gtk.HBox()
		self.inside_applet.pack_start(self.icon)
		self.inside_applet.pack_start(self.temp)
		
		# Creates tooltip
		self.tooltip = gtk.Tooltips()
		self.update_tooltip()
		
		# Adds hbox to eventbox
		event_box.add(self.inside_applet)
		app_window.add(event_box)
		app_window.show_all()
		return event_box

	def menu_set(self):
		
		if self.alarm_enabled:
			self.applet.setup_menu_from_file (glob.resources_dir, "computertemp_menu2.xml", "computertemp", self.verbs)
		else:
			self.applet.setup_menu_from_file (glob.resources_dir, "computertemp_menu.xml", "computertemp", self.verbs)


	def menu_alarm_toggled(self, event, data=None):

		self.alarm_enabled = not self.alarm_enabled

		self.menu_set()
		
		self.prefs.alarm_enabled_check.set_active(self.alarm_enabled)
		self.prefs.alarm_enabled_check_toggled(None)

		
	# About menu
	def about_info(self,event,data=None):

		about = gtk.AboutDialog()
		about.set_name(glob.name_long)
		about.set_version(glob.version)
		about.set_authors(glob.authors)
		about.set_artists(glob.artists)
		about.set_translator_credits(_('translator-credits'))
		about.set_logo(gtk.gdk.pixbuf_new_from_file(glob.pixmaps_dir+"/computertemp.png"))
		about.set_license(glob.license)
		about.set_wrap_license(True)
		about.set_copyright(glob.copyright)

		def openHomePage(widget,url,url2):
			import webbrowser
			webbrowser.open_new(url)

		gtk.about_dialog_set_url_hook(openHomePage,glob.website)
		about.set_website(glob.website)
		about.run()
		about.destroy()

		
	# Hello!
	def __init__(self,applet,iid):

		# Applet as a gboject
		self.__gobject_init__()
		
		self.applet = applet
		
		# Init variables
		self.log_filename_default = '{home}/logs/{sensor}_{date}.log'
		self.log_info_default = '{date} {time}#{sensor}#{zone}#{temp}'
		self.log_filename = self.log_filename_default
		self.log_info = self.log_info_default
		self.logging = False
		self.autologname = True
		self.sensor = 0
		self.tempmon_enabled = False
		self.thermal_zones = []
		self.thermalzone = ''
		self.tempzone = 0
		self.timeout = 5000
		self.timeout_count = 1
		self.timeout_log = 5000
		self.timeout_log_count = 1
		self.min_temp = 40
		self.max_temp = 80
		self.visualization_mode = 0		# 0 = Graphic   1 = Text   2 = Graphic and Text
		self.visualization_units = 0		# 0 = Celsius    1 = Farenheit
		self.alarm_enabled = False
		self.alarm_limit = 80
		self.alarm_when = 1				# 0 = Smaller   1 = Greater
		self.alarm_command = ''
		self.alarm_running = False
		self.alarm_alive = False
		self.alarm_pid = 0
		self.alarm_repeat = False
		self.debug = False
		self.icon_path = ''
		self.tips_logname = ''
		self.tips_loginfo = ''

		# GConf stuff init for preferences
		self.gconf = gconf.ComputertempGConf(self)
		print "Applet GConf id:", self.gconf.get_applet_name()
		self.gconf.read_prefs()
		self.gconf.save_prefs_all()
		self.setlogfilename()
		self.setloginfo()
		self.init_log_tooltips()
		
		# Set Debug info via commandline
		if DEBUG:
			self.debug = True
			self.gconf.save_prefs_debug()

		# Init Temperature Monitor functions
		self.tempmon = tempf.TempFuncs(self)

		# Lets create the gui
		self.box = self.create_applet()
		self.change_orientation(None, None) # Forcing to get panel position
		self.prefs = prefs.ComputertempPrefs(self)
		
		# Display error if there are no sensors enabled
		if not self.tempmon_enabled: self.dialog(_('\nThere is not Thermal Monitor support on your machine!!!'))
		
		# Init context menu stuff
		self.verbs = [("Alarm", self.menu_alarm_toggled),
					  ("Prefs", self.prefs.preferences_show), 
					  ("About", self.about_info)]
		self.menu_set()
			
		# Show icon
		self.update_icon()
			
		# Callbacks for timeout and change_background and orientation
		self.timeout_source = gobject.timeout_add (1000, self.update_main)
		self.applet.connect("change_background", self.change_background)
		self.applet.connect("change-orient", self.change_orientation)

gobject.type_register(computertempApplet)	

DEBUG = False

# Bonobo factory of computertempApplet
def computertemp_applet_factory(applet, iid):
	computertempApplet(applet, iid)
	return True

# Main method. Decide if we should run computertemp as applet or systray icon
def main(debug):
	
	global DEBUG
	DEBUG = debug
	
	# Create the applet
	gnomeapplet.bonobo_factory("OAFIID:GNOME_ComputertempApplet_Factory",
				   computertempApplet.__gtype__,
				   glob.name,
				   glob.version,
				   computertemp_applet_factory)