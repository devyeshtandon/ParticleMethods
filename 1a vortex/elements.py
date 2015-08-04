import numpy as np
import cmath as cm
import math

pi = math.pi

def vortex_source_field(strength, new_coods):
	distance = [abs(i) for i in new_coods]
	temp = [0 for i in distance]
	for i in range(len(distance)):
		if distance[i] != 0:
			temp[i] = strength*1.0/2/pi/(distance[i])
		else:
			temp[i] = 0+0*1j
	return temp

def doublet_field(strength, new_coods, direction):
	temp = [0 for i in new_coods]
	for i in range(len(new_coods)):
		print new_coods[i]
		distance = abs(new_coods[i])
		print distance
		if distance != 0:
			temp[i] = strength*1.0/2/pi/pow(distance,2)
			if direction == "t":
				temp[i] = (temp[i]*cm.sin(new_coods[i]))
			if direction == "r":
				temp[i] = -(temp[i]*cm.cos(new_coods[i]))

		else:
			temp[i] = 0+0*1j
	return temp

def direction(array, value):
	temp = [0 for i in (array)]
	for i in range(len(array)):
		distance = abs(array[i])
		if distance != 0:
			if value == "tangential":
				temp[i] = (-array[i].imag + array[i].real*1j)/distance
			elif value == "radial":
				temp[i] = array[i]/distance
			else:
				temp[i] = [ (-array[i].imag + array[i].real*1j)/distance, 
					 array[i]/distance]
		else:
			temp[i] = 0 + 0*1j
	return (temp)

def vortex(element, target, *argv):
	strength  = element.strength
	if len(argv) == 1:
		location = element.updatexy
	else:
		location  = element.xy

	new_coods = [(i - location) for i in target]

	if element.ele_type == "vortex":
		field_mag = vortex_source_field(strength, new_coods)   
		field_dir = direction(new_coods, "tangential")
	elif element.ele_type == "source":
		field_mag = vortex_source_field(strength, new_coods)   
		field_dir = direction(new_coods, "radial")
	elif element.ele_type == "uniform":
		fielf_mag = strength
		field_dir = 1
	elif element.ele_type == "doublet":
		field_mag_t = doublet_field(strength, new_coods, "t")
		field_mag_r = doublet_field(strength, new_coods, "r")
		field_dir_t = direction(new_coods, "tangential")
		field_dir_r = direction(new_coods, "radial")
	
	if element.ele_type == "doublet":
		field_tot = [field_mag_t[i]*field_dir_t[i] +  field_mag_r[i]*field_dir_r[i] for i in range(len(new_coods))]
	else:
		field_tot = [field_mag[i]* field_dir[i] for i in range(len(new_coods))]
	
#	print field_tot
#	raw_input()
	return (field_tot);

