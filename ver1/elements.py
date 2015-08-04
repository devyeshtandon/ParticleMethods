# Functions Defined here
import numpy as np
import math

pi = math.pi
def radius(array):
	return [np.sqrt(np.dot(i,i)) for i in array]

def invert(array):
	temp = [0 for i in array];
	for i in range(len(array)):
		if array[i] == 0:
			temp[i] = 0
		else:		
			temp[i] = 1.0/array[i] 
	return temp;

def tangential(array):
	temp = [0 for i in array]
	for i in range(len(array)):
		norm = np.sqrt(array[i][0]**2 + array[i][1]**2)
		if norm == 0.0:
			temp[i] = (0.0,0.0)
		else:
			temp[i] = (-array[i][1]/norm, array[i][0]/norm)
#		print temp[i]
	return (temp)

def vortex(strength, location, target):
	new_coods = [np.subtract(i, location) for i in target]
#	print new_coods
	distances = radius(new_coods)
#	print distances
	field_mag = np.multiply((1.0*strength/2/pi),invert(distances[:]))
#	print field_mag
	field_dir = tangential(new_coods)
#	print field_dir
	field_tot = ([np.multiply(field_mag[i], field_dir[i]) for i in range(len(distances))])
#	print np.asarray(field_tot)
	return (field_tot);
