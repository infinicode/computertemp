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

		self.thermal_path = '/sys/devices/platform/windfarm.0/'
		self.thermal_suffix = '-temp'
		self.sensors = (['cpu','CPU'], ['gpu','GPU'], ['sensor1','Sensor1'], ['sensor2','Sensor2'])
		self.all_sensors = []
		self.sensors_display_name = []

		for i in self.sensors:
			if os.path.exists(self.thermal_path + i[0] + self.thermal_suffix):
				self.all_sensors.append(i[0])
				self.sensors_display_name.append(i[1])

	# Get the name of the hardware sensor
	def get_sensor_name(self): return 'G5 Windfarm'

	# Is there Thermal Monitor support on machine?
	def temp_support(self):
		return os.path.isdir(self.thermal_path) and self.all_sensors != []

	# Return a list with the thermal zones availables
	def get_zones(self):
		if self.temp_support():
			return list(self.all_sensors)

	# Return zone name at position num
	def get_zone_name(self, num):
		if self.temp_support():
			return self.all_sensors[num]
		else: return None

	# Return zone name to display at position num
	def get_zone_display_name(self, num):
		if self.temp_support():
			return self.sensors_display_name[num]


	# Reads temperature from zone
	def get_zone_temp(self, zone):
		if self.temp_support():
			try:
				fproc = open(self.thermal_path + zone + self.thermal_suffix, "r")
				temp = int(float(fproc.readline()))
				fproc.close()
				return temp
			except:
				return None
			else:
				return 0

