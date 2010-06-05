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

class TempFuncs:

	def __init__(self):
		
		self.thermal_path = '/proc/acpi/ibm/'
		self.thermal_file = '/thermal'
		self.sensors = range(8)
		self.sensors_names = ('CPU', 'Mini-PCI', 'HDD', 'GPU', 'Main Battery', 'Bay Battery', 'Main Battery', 'Bay Battery')

	# Get the name of the hardware sensor
	def get_sensor_name(self): return 'IBM ACPI'

	# Is there Thermal Monitor support on machine?
	def temp_support(self):
		return os.path.isdir(self.thermal_path)

	# Return a list with the thermal zones availables
	def get_zones(self):
		if self.temp_support():
			return self.sensors
	
	# Return zone name at position num
	def get_zone_name(self, num):
		if self.temp_support():
			return self.sensors[num]
		else: return None

	# Return zone name to display at position num
	def get_zone_display_name(self, num):
		if self.temp_support():
			return self.sensors_names[num]
		
	
	# Reads temperature from acpi_ibm
	# cat /proc/acpi/ibm/thermal 
	# temperatures: 44 41 33 42 33 -128 30 -128 
	def get_zone_temp(self, zone):
		if self.temp_support():
			try:
				fproc = open(self.thermal_path + self.thermal_file,"r")
				temp =  fproc.readline()
				fproc.close()
				temp = temp.split()
				return temp[zone+1]
			except:
				return None
			else:
				return 0
			
