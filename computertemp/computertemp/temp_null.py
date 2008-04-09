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



# No Thermal Monitor Support
class TempFuncs:

	# Lets try to see which backend are we using
	def __init__(self): pass
	
	# Get the name of the hardware sensor
	def get_sensor_name(self): return 'None!'
	
	# Is there Thermal Monitor support on machine?
	def temp_support(self): return False

	# Return a list with the thermal zones availables
	def get_zones(self): return None

	# Return zone name at position num
	def get_zone_name(self, num): return None
	
	# Return zone name to display at position num
	def get_zone_display_name(self, num): return None

	# Reads temperature from zone
	def get_zone_temp(self, zone): return None
