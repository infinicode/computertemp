# -*- coding: UTF-8 -*-

"""
Copyright (C) 2005-2008 Adolfo González Blázquez <code@infinicode.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

If you find any bugs or have any suggestions email: code@infinicode.org
"""

import gconf

class ComputertempGConf:

	def __init__(self, app):
	
		self.app = app
		self.applet = app.applet

		self.gconf_path	  = "/apps/computertemp"
		self.gconf_client = gconf.client_get_default()
		
		self.gconf_applet = self.applet.get_preferences_key()
		
		self.gconf_key_sensor				= self.gconf_applet + '/sensor'
		self.gconf_key_thermalzone			= self.gconf_applet + '/thermal_zone'
		self.gconf_key_visualization_mode	= self.gconf_applet + '/visualization_mode'
		self.gconf_key_visualization_units	= self.gconf_applet + '/visualization_units'
		self.gconf_key_timeout				= self.gconf_applet + '/timeout'
		self.gconf_key_timeout_log			= self.gconf_applet + '/timeout_log'
		self.gconf_key_min_temp				= self.gconf_applet + '/min_temp'
		self.gconf_key_max_temp				= self.gconf_applet + '/max_temp'
		self.gconf_key_logging				= self.gconf_applet + '/logging'
		self.gconf_key_autologname			= self.gconf_applet + '/autologname'
		self.gconf_key_log_filename			= self.gconf_applet + '/log_filename'
		self.gconf_key_log_info				= self.gconf_applet + '/log_info'
		self.gconf_key_alarm_enabled		= self.gconf_applet + '/alarm_enabled'
		self.gconf_key_alarm_limit			= self.gconf_applet + '/alarm_limit'
		self.gconf_key_alarm_when			= self.gconf_applet + '/alarm_when'
		self.gconf_key_alarm_command		= self.gconf_applet + '/alarm_command'
		self.gconf_key_alarm_repeat			= self.gconf_applet + '/alarm_repeat'
		self.gconf_key_debug				= self.gconf_applet + '/debug'
		
		self.applet.add_preferences("/schemas" + self.gconf_path)
		self.gconf_client.add_dir(self.gconf_applet, gconf.CLIENT_PRELOAD_NONE)
		
		self.gconf_client.notify_add(self.gconf_key_sensor, self.preferences_sensor_changed)
		self.gconf_client.notify_add(self.gconf_key_thermalzone, self.preferences_thermalzone_changed)
		self.gconf_client.notify_add(self.gconf_key_visualization_mode, self.preferences_visualization_mode_changed)
		self.gconf_client.notify_add(self.gconf_key_visualization_units, self.preferences_visualization_units_changed)
		self.gconf_client.notify_add(self.gconf_key_timeout, self.preferences_timeout_changed)
		self.gconf_client.notify_add(self.gconf_key_timeout_log, self.preferences_timeout_log_changed)
		self.gconf_client.notify_add(self.gconf_key_min_temp, self.preferences_min_temp_changed)
		self.gconf_client.notify_add(self.gconf_key_max_temp, self.preferences_max_temp_changed)
		self.gconf_client.notify_add(self.gconf_key_logging, self.preferences_logging_changed)
		self.gconf_client.notify_add(self.gconf_key_autologname, self.preferences_autologname_changed)
		self.gconf_client.notify_add(self.gconf_key_log_filename, self.preferences_log_filename_changed)
		self.gconf_client.notify_add(self.gconf_key_log_info, self.preferences_log_info_changed)
		self.gconf_client.notify_add(self.gconf_key_alarm_enabled, self.preferences_alarm_enabled_changed)
		self.gconf_client.notify_add(self.gconf_key_alarm_limit, self.preferences_alarm_limit_changed)
		self.gconf_client.notify_add(self.gconf_key_alarm_when, self.preferences_alarm_when_changed)
		self.gconf_client.notify_add(self.gconf_key_alarm_command, self.preferences_alarm_command_changed)
		self.gconf_client.notify_add(self.gconf_key_alarm_repeat, self.preferences_alarm_repeat_changed)
		self.gconf_client.notify_add(self.gconf_key_debug, self.preferences_debug_changed)
		
		
	# Get preferences using GConf
	def read_prefs(self):
		
		temp = self.gconf_client.get_int(self.gconf_key_sensor)
		if temp != None: self.app.sensor = temp
		
		temp = self.gconf_client.get_int(self.gconf_key_thermalzone)
		if temp != None: self.app.thermalzone = temp
		
		temp = self.gconf_client.get_int(self.gconf_key_visualization_mode)
		if temp != None: self.app.visualization_mode = temp
			
		temp = self.gconf_client.get_int(self.gconf_key_visualization_units)
		if temp != None: self.app.visualization_units = temp
			
		temp = self.gconf_client.get_int(self.gconf_key_timeout) * 1000
		if temp != None and temp > 0: self.app.timeout = temp
		
		temp = self.gconf_client.get_int(self.gconf_key_timeout_log) * 1000
		if temp != None and temp > 0: self.app.timeout_log = temp

		temp = self.gconf_client.get_int(self.gconf_key_min_temp)
		if temp != None: self.app.min_temp = temp
			
		temp = self.gconf_client.get_int(self.gconf_key_max_temp)
		if temp != None: self.app.max_temp = temp
			
		temp = self.gconf_client.get_bool(self.gconf_key_logging)
		if temp != None: self.app.logging = temp
			
		temp = self.gconf_client.get_bool(self.gconf_key_autologname)
		if temp != None: self.app.autologname = temp
			
		temp = self.gconf_client.get_string(self.gconf_key_log_filename)
		if temp != None: self.app.log_filename = temp
		
		temp = self.gconf_client.get_string(self.gconf_key_log_info)
		if temp != None: self.app.log_info = temp
			
		temp = self.gconf_client.get_bool(self.gconf_key_alarm_enabled)
		if temp != None: self.app.alarm_enabled = temp
		
		temp = self.gconf_client.get_int(self.gconf_key_alarm_limit)
		if temp != None: self.app.alarm_limit = temp
		
		temp = self.gconf_client.get_int(self.gconf_key_alarm_when)
		if temp != None: self.app.alarm_when = temp
		
		temp = self.gconf_client.get_string(self.gconf_key_alarm_command)
		if temp != None: self.app.alarm_command = temp
		
		temp = self.gconf_client.get_bool(self.gconf_key_alarm_repeat)
		if temp != None: self.app.alarm_repeat = temp
		
		temp = self.gconf_client.get_bool(self.gconf_key_debug)
		if temp != None: self.app.debug = temp

		
	# Save every preference to GConf
	def save_prefs_all(self):

		self.save_prefs_sensor()
		self.save_prefs_thermalzone()
		self.save_prefs_visualization_mode()
		self.save_prefs_visualization_units()
		self.save_prefs_timeout()
		self.save_prefs_timeout_log()
		self.save_prefs_min_temp()
		self.save_prefs_max_temp()
		self.save_prefs_logging()
		self.save_prefs_autologname()
		self.save_prefs_log_filename()
		self.save_prefs_log_info()
		self.save_prefs_alarm_enabled()
		self.save_prefs_alarm_limit()
		self.save_prefs_alarm_when()
		self.save_prefs_alarm_command()
		self.save_prefs_alarm_repeat()
		self.save_prefs_debug()


	def save_prefs_sensor(self):
		self.gconf_client.set_int(self.gconf_key_sensor, self.app.sensor)

	def save_prefs_thermalzone(self):
		self.gconf_client.set_int(self.gconf_key_thermalzone, self.app.thermalzone)
		
	def save_prefs_visualization_mode(self):
		self.gconf_client.set_int(self.gconf_key_visualization_mode, self.app.visualization_mode)
		
	def save_prefs_visualization_units(self):
		self.gconf_client.set_int(self.gconf_key_visualization_units, self.app.visualization_units)
		
	def save_prefs_timeout(self):
		self.gconf_client.set_int(self.gconf_key_timeout, self.app.timeout/1000)
		
	def save_prefs_timeout_log(self):
		self.gconf_client.set_int(self.gconf_key_timeout_log, self.app.timeout_log/1000)
		
	def save_prefs_min_temp(self):
		self.gconf_client.set_int(self.gconf_key_min_temp, self.app.min_temp)
		
	def save_prefs_max_temp(self):
		self.gconf_client.set_int(self.gconf_key_max_temp, self.app.max_temp)
	
	def save_prefs_logging(self):
		self.gconf_client.set_bool(self.gconf_key_logging, self.app.logging)
		
	def save_prefs_autologname(self):
		self.gconf_client.set_bool(self.gconf_key_autologname, self.app.autologname)
		
	def save_prefs_log_filename(self):
		self.gconf_client.set_string(self.gconf_key_log_filename, self.app.log_filename)
		
	def save_prefs_log_info(self):
		self.gconf_client.set_string(self.gconf_key_log_info, self.app.log_info)
		
	def save_prefs_alarm_enabled(self):
		self.gconf_client.set_bool(self.gconf_key_alarm_enabled, self.app.alarm_enabled)

	def save_prefs_alarm_limit(self):
		self.gconf_client.set_int(self.gconf_key_alarm_limit, self.app.alarm_limit)

	def save_prefs_alarm_when(self):
		self.gconf_client.set_int(self.gconf_key_alarm_when, self.app.alarm_when)
		
	def save_prefs_alarm_command(self):
		self.gconf_client.set_string(self.gconf_key_alarm_command, self.app.alarm_command)

	def save_prefs_alarm_repeat(self):
		self.gconf_client.set_bool(self.gconf_key_alarm_repeat, self.app.alarm_repeat)
		
	def save_prefs_debug(self):
		self.gconf_client.set_bool(self.gconf_key_debug, self.app.debug)
	
	# Monitoring changes using gconf editor
	def preferences_sensor_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			self.app.sensor = entry.get_value().get_int()
			self.app.update_icon()
			self.app.update_text()
			self.app.update_tooltip()

	# Monitoring changes using gconf editor
	def preferences_thermalzone_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			self.app.thermalzone = entry.get_value().get_int()
			self.app.update_icon()
			self.app.update_text()
			self.app.update_tooltip()

	def preferences_visualization_mode_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			self.app.visualization_mode = entry.get_value().get_int()
			self.app.update_icon()
			self.app.update_text()
			self.app.update_tooltip()
		
	def preferences_visualization_units_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			self.app.visualization_units = entry.get_value().get_int()
			self.app.update_icon()
			self.app.update_text()
			self.app.update_tooltip()
		
	def preferences_timeout_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			self.app.timeout = entry.get_value().get_int() * 1000
			self.app.timeout_count = 0
			
	def preferences_timeout_log_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			self.app.timeout_log = entry.get_value().get_int() * 1000
		
	def preferences_min_temp_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			temp = entry.get_value().get_int()
			if temp >= self.app.max_temp:
				self.app.min_temp = self.app.max_temp - 1
				self.gconf_client.set_int(self.gconf_key_min_temp, self.app.max_temp - 1)
			else:
				self.app.min_temp = temp
			if self.app.prefs: self.app.prefs.spinmin.set_value(self.app.min_temp)
			self.app.update_icon()
			self.app.update_text()
			self.app.update_tooltip()
		
	def preferences_max_temp_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			temp = entry.get_value().get_int()
			if temp <= self.app.min_temp:
				self.app.max_temp = self.app.min_temp + 1
				self.gconf_client.set_int(self.gconf_key_max_temp, self.app.min_temp + 1)
			else:
				self.app.max_temp = temp
			if self.app.prefs: self.app.prefs.spinmax.set_value(self.app.max_temp)
			self.app.update_icon()
			self.app.update_text()
			self.app.update_tooltip()

	def preferences_logging_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_BOOL:
			self.app.logging = entry.get_value().get_bool()
					
	def preferences_autologname_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_BOOL:
			self.app.autologname = entry.get_value().get_bool()
			self.app.timeout_log_count = 0
		
	def preferences_log_filename_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_STRING:
			self.app.log_filename = entry.get_value().get_string()
			if self.app.prefs: self.app.prefs.logentry.set_text(self.app.log_filename)
			self.app.timeout_log_count = 0

	def preferences_log_info_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_STRING:
			self.app.log_info = entry.get_value().get_string()
			if self.app.prefs: self.app.prefs.logformat_entry.set_text(self.app.log_info)
			self.app.timeout_log_count = 0
			
	def preferences_alarm_enabled_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_BOOL:
			self.app.alarm_enabled = entry.get_value().get_bool()
			self.app.reset_alarm()

	def preferences_alarm_limit_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			self.app.alarm_limit = entry.get_value().get_int()
			self.app.reset_alarm()
		
	def preferences_alarm_when_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_INT:
			self.app.alarm_when = entry.get_value().get_int()
			self.app.reset_alarm()
			
	def preferences_alarm_command_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_STRING:
			self.app.alarm_command = entry.get_value().get_string()
			if self.app.prefs: self.app.prefs.alarm_command_entry.set_text(self.app.alarm_command)
			self.app.reset_alarm()

	def preferences_alarm_repeat_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_BOOL:
			self.app.alarm_repeat = entry.get_value().get_bool()
			self.app.reset_alarm()
			
	def preferences_debug_changed(self, client, connection_id, entry, args):
		if entry.get_value() != None and entry.get_value().type == gconf.VALUE_BOOL:
			self.app.debug = entry.get_value().get_bool()
			self.app.update_tooltip()


	# Returns applet name for GConf
	def get_applet_name(self):
		name = self.gconf_applet.split('/')
		return name[4]