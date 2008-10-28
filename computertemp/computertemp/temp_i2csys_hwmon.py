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
import dircache
import re

class TempFuncs:

	def __init__(self):
	
		self.thermal_path = '/sys/class/hwmon/'
		
		if os.path.isdir(self.thermal_path): 
			self.i2csensors = dircache.listdir(self.thermal_path)
		

	# Get the name of the hardware sensor
	def get_sensor_name(self): return 'Kernel i2c sensors (hwmon)'

	# Is there acpi thermal_zone support on machine?
	def temp_support(self):
		return os.path.isdir(self.thermal_path) and self.i2csensors != []


	# Return a list with the thermal zones availables
	def get_zones(self): 
		if self.temp_support():
			zones = []
			for i in xrange(len(self.i2csensors)):
				lista = (dircache.listdir(self.thermal_path+self.i2csensors[i]+'/device'))
				for j in xrange(len(lista)):
					if re.search('temp[0-9]*_input', lista[j]) != None:
						zones.append(self.i2csensors[i]+'/device/'+lista[j])
				
			return zones
		else: return None


	# Return zone name at position num
	def get_zone_name(self, num):
		if self.temp_support():
			return self.get_zones()[num]
		else: return None

		
	# Return zone name to display at position num
	def get_zone_display_name(self, num):
		tmp = self.get_zone_name(num).split('/')
		num = tmp[2].lstrip('temp')
		num = num.rstrip('_input')
		return tmp[0] + " (" + num + ")"


	# Reads temperature from zone
	def get_zone_temp(self, zone):
		if self.temp_support():
			try:
				fproc = open(self.thermal_path + zone,"r")
				temp =  fproc.readline()
				fproc.close()
				return int(temp) / 1000
			except IOError:
				return None
		else:
			return 0
