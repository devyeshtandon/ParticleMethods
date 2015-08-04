import numpy as np
import cmath
import math

pi = math.pi
def vortex_field_generation(strength, distance):
	temp = [0 for i in distance]
	for i in range(len(distance)):
		if distance[i] != 0:
			temp[i] = strength*1.0/2/pi*math.log(distance[i])
		else:
			temp[i] = 0+0*1j
	return temp

def source_field_generation(strength, distance):
	temp = [0 for i in distance]
	for i in range(len(distance)):
		if distance[i] != 0:
			temp[i] = strength*1.0/2/pi/distance[i]
		else:
			temp[i] = 0+0*1j
	return temp

def tangential(array):
	temp = [0 for i in array]
	for i in range(len(array)):
		if abs(array[i]) != 0:
			temp[i] = (-array[i].imag + array[i].real*1j)/abs(array[i])
		else:
			temp[i] = 0 + 0*1j
	return (temp)

def radial(array):
	temp = [0 for i in array]
	for i in range(len(array)):
		if abs(array[i]) != 0:
			temp[i] = array[i]/abs(array[i])
		else:
			temp[i] = 0 + 0*1j
	return (temp)


def vortex(strength, location, target):
	new_coods = [(i - location) for i in target]
	distances = [abs(i) for i in new_coods]
	field_mag = vortex_field_generation(strength, distances)   
	field_dir = tangential(new_coods)
	field_tot = [(field_mag[i]* field_dir[i]) for i in range(len(distances))]
	return (field_tot);

def source(strength, location, target):
	new_coods = [(i-location) for i in target]
	distances = [abs(i) for i in new_coods]
	field_mag = source_field_generation(strength, distances)
	field_dir = radial(new_coods)
	field_tot = [(field_mag[i]*field_dir[i]) for i in range(len(distances))]
	return field_tot
