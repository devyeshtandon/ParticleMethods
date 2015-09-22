import numpy as np
import time
import pylab
import math
import cmath
from elements import vortex

pi = math.pi
class particle:
	xy       = (0.0,0);
	updatexy = xy;

class elemental:
	xy       = (0,0);
	strength = 1;
	fixed    = 0;
	updatexy = xy;
	

############################################################################
# Counts
############################################################################

num_of_vortex = 2
num_of_particles = 0

num_of_targets = num_of_vortex + num_of_particles

############################################################################
# Elements Defined
############################################################################

vort = [elemental() for i in range(num_of_vortex)]

#Vortex 1
vort[0].xy       = -5 + 0*1j
vort[0].strength = 1;
vort[0].updatexy = vort[0].xy
vort[0].fixed    = 0

#Vortex 2
vort[1].xy       = 5 + 0j
vort[1].strength = 1;
vort[1].updatexy = vort[1].xy

#Vortex 3
#vort[2].xy       = (0.0,0.5)
#vort[2].strength = 0;
#vort[2].updatexy = vort[2].xy

#############################################################################
# Target and Field Dev
#############################################################################

field  = [[0 for x in range(num_of_vortex)] for x in range(num_of_targets)]
field2 = [[0 for x in range(num_of_vortex)] for x in range(num_of_targets)]

#############################################################################
# Plotting
#############################################################################

pylab.ion()
line, = pylab.plot(0,1,'ro',markersize=6)
pylab.axis([-5,5,5,-5])

line.set_xdata(0)
line.set_ydata(0)
pylab.draw()

#############################################################################
# Simulation criteria
#############################################################################

sim_time = 1200;
dt       = 1;
time     = pylab.arange(0, sim_time, dt)


X = [0]
Y = [1]

#############################################################################
# Simulation
#############################################################################
for t in time:
	
	target = [vort[i].updatexy for i in range(num_of_vortex)]
	target.extend(part[i].updatexy for i in range(num_of_particles))

#	print target

	for i in range(num_of_vortex):
		field[i][:] = vortex(vort[i].strength, vort[i].updatexy, target)

	print field

	for i in range(num_of_targets):
		for j in range(num_of_targets):
			if vort[i].fixed == 0:
				vort[i].updatexy = field[j][i]*dt + vort[i].updatexy

#	print field[1][0]
#	print vort[1].updatexy

#	target = [vort[i].updatexy for i in range(num_of_vortex)]
#	target.extend(part[i].updatexy for i in range(num_of_particles))

#	for i in range(num_of_vortex):
#		field2[i][:] = vortex(vort[i].strength, vort[i].updatexy, target)
#	print field2
	
#	for i in range(len(vort)):
#		for j in range(num_of_targets):
#			if vort[i].fixed == 0:
#				vort[i].xy = vort[i].update(np.multiply(field[j][i], dt/2))
#				vort[i].xy = vort[i].update(np.multiply(field2[j][i], dt/2))

#	X.extend([(vort[1].xy)[0]])
#	Y.extend([(vort[1].xy)[1]])
#	line.set_xdata(X)
#	line.set_ydata(Y)

	line.set_xdata([vort[i].updatexy.real for i in range(num_of_vortex)] )
	line.set_ydata([vort[i].updatexy.imag for i in range(num_of_vortex)] )
	print abs(vort[0].updatexy)
	pylab.draw()
#	raw_input()
raw_input()

	
