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

from telnetlib import Telnet

class TempFuncs:

	def __init__(self):
	
		self.host = 'localhost'
		self.port = 7634
		
		self.get_data()

	# Read data from hddtemp telnet interface
	def get_data(self):
		self.hds = []
		try:
			tn = Telnet(self.host, self.port)
			data = tn.read_all()
			data = unicode(data, errors='ignore')
			data = data.replace('\x10', '')
			tn.close()
			data = data.split('||')
			for i in data: self.hds.append(i.lstrip('|').rstrip('|').split('|'))
		except:
			self.hds = None

	# Get the name of the hardware sensor
	def get_sensor_name(self): return 'HDDTEMP'

	# Is there acpi thermal_zone support on machine?
	def temp_support(self):
		if self.hds != None: return True
		else: return False


	# Return a list with the thermal zones availables
	def get_zones(self): 
		if self.temp_support():
			return range(len(self.hds))


	# Return zone name at position num
	def get_zone_name(self, num):
		if self.temp_support():
			return num
		else: return None

		
	# Return zone name to display at position num
	def get_zone_display_name(self, num):
		return self.hds[num][1] + ' (' + self.hds[num][0] + ')'


	# Reads temperature from zone
	def get_zone_temp(self, zone):
		if self.temp_support():
			self.get_data()
			return self.hds[int(zone)][2]
		else:
			return 0
