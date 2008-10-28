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

import os.path

# This class is a wrapper for the different thermal monitor backends
class TempFuncs:

	# Lets try to see which backend are we using
	def __init__(self, app):
		
		self.app = app
		self.sensors = []
		
		self.get_active_sensors()
		
		if len(self.sensors) > 0: 
			self.set_sensor_active(self.sensors[self.app.sensor][0])
		else:
			self.set_sensor_active(None)
		
	# Lets see which sensors are enabled
	def get_active_sensors(self):
		
		import temp_acpi as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_acpi']); del t

		import temp_adt746x as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_adt746x']); del t
		
		import temp_hddtemp as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_hddtemp']); del t

		import temp_i2csys as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_i2csys']); del t

		import temp_i2csys_hwmon as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_i2csys_hwmon']); del t
		
		import temp_i8k as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_i8k']); del t
		
		import temp_ibmacpi as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_ibmacpi']); del t
		
		import temp_omnibook as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_omnibook']); del t
		
		import temp_windfarm as module; t = module.TempFuncs()
		if t.temp_support(): self.sensors.append([t.get_sensor_name(),'temp_windfarm']); del t

	# Enable selected hardware sensor
	def set_sensor_active(self, sensor):
		
		from computertemp import temp_null as funcs
		for i in self.sensors:
			if sensor in i: funcs = __import__(i[1], globals(), locals(), ['computertemp'])
			
		self.tempfuncs = funcs.TempFuncs()
		self.init_sensor()
		print "Hardware Sensor Enabled:", self.tempfuncs.get_sensor_name()
		
	# Load needed variables for hardware sensor init
	def init_sensor(self):

		self.app.tempmon_enabled = self.tempfuncs.temp_support()
		self.app.thermal_zones = self.tempfuncs.get_zones()
		self.app.tempmon_enabled = self.app.tempmon_enabled and self.app.thermal_zones != []
		if self.app.tempmon_enabled:    
			self.app.data = self.tempfuncs.get_zone_temp(self.tempfuncs.get_zone_name(self.app.thermalzone))
		else:
			self.app.data = "XX"

################################################################
# COMMON FUNCTIONS FOR ALL SUBMODULES
	
	# Get the name of the hardware sensor
	# Out: string with the name of the hardware sensor
	def get_sensor_name(self): return self.tempfuncs.get_sensor_name()
	
	# Is there Thermal Monitor support on hardware sensor?
	# Out: True || False
	def temp_support(self): return self.sensor_available and self.tempfuncs.temp_support()

	# Return a list with the thermal zones availables
	# Out: list of thermal zones (for preferences combobox)
	def get_zones(self): return self.tempfuncs.get_zones()

	# Return zone name at position num
	# In  : number of thermal zone to monitor
	# Out : name of the zone to monitor (file to read)
	def get_zone_name(self, num): return self.tempfuncs.get_zone_name(num)
	
	# Return zone name to display at position num
	# In  : number of thermal zone to monitor
	# Out : name of the zone to monitor (for displaying on combobox and tooltip)
	def get_zone_display_name(self, num): return self.tempfuncs.get_zone_display_name(num)
	
	# Reads temperature from zone
	# In  : zone number
	# Out : temparature
	def get_zone_temp(self, zone): return self.tempfuncs.get_zone_temp(zone)
