# -*- coding: UTF-8 -*-

# +-------------------------------------------------------------------------------------+
# | GPL											|
# +-------------------------------------------------------------------------------------+
# | Copyright (c) 2005,2006 Adolfo González Blázquez <code@infinicode.org>	|
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

import os.path

class TempFuncs:

	def __init__(self):
		
		self.thermal_path = '/proc/omnibook/temperature'

	# Get the name of the hardware sensor
	def get_sensor_name(self): return 'Omnibook'

	# Is there Thermal Monitor support on machine?
	def temp_support(self):
		return os.path.isfile(self.thermal_path)

	# Return a list with the thermal zones availables
	def get_zones(self):
		if self.temp_support():
			return ('1') # We need to return a tuple
	
	# Return zone name at position num
	def get_zone_name(self, num):
		if self.temp_support():
			return 1
		else: return None

	# Return zone name to display at position num
	def get_zone_display_name(self, num):
		if self.temp_support():
			return 'CPU'
		
	
	# Reads temperature from omnibook kernel module
	def get_zone_temp(self, zone):
		if self.temp_support():
			try:
				fproc = open(self.thermal_path,"r")
				temp =  fproc.readline()
				fproc.close()
				temp = temp.split()
				return temp[2]
			except IOError:
				return None
			else:
				return 0
			
