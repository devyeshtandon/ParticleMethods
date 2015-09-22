import numpy as np
from pylab import arange
import pylab
import math
import cmath
from elements import vortex

pi = math.pi

class elemental:
	xy       = 0;
	strength = 5;
	fixed    = 0;
	updatexy = xy;
	ele_type = "vortex"
	
	def location(self, x):
		self.xy = x
		self.updatexy = self.xy
	
	def update(self):
		self.updatexy = self.xy
	
############################################################################
# Counts
############################################################################

num_of_vortex    = 3
num_of_particles = 0
num_of_targets   = num_of_vortex + num_of_particles

############################################################################
# Elements Defined
############################################################################

def reflection(point):
	temp = abs(point)
	mag = 1/cmath.sqrt(temp)
	P = mag*cmath.exp(math.atan2(point.imag,point.real))
	return P
vort = [elemental() for i in range(num_of_targets)]

vort[0].location(0)
vort[0].fixed =1
vort[1].location(1.25)
vort[2].location(reflection(1.25))
vort[2].fixed = 0
#############################################################################
# Target and Field Dev
#############################################################################

field  = [[0 for x in range(num_of_vortex)] for x in range(num_of_targets)]
field2 = [[0 for x in range(num_of_vortex)] for x in range(num_of_targets)]

#############################################################################
# Plotting
#############################################################################

pylab.ion()
line, = pylab.plot(0,1, 'ro')
pylab.axis([-2,2,2,-2])

line.set_xdata(0)
line.set_ydata(0)
pylab.draw()

#############################################################################
# Simulation criteria
#############################################################################

dt       = 0.01 ;
sim_time = 5;
time     = pylab.arange(0, sim_time, dt)

X = []
Y = []

alpha = 0.5

#############################################################################
# Simulation
#############################################################################
for t in time:
	X = reflection(vort[1].xy)
	vort[2].xy = X
	vort[2].updatexy = X
	vort[2].strength = -vort[1].strength/abs(vort[1].xy)

	vort[0].strength = -vort[2].strength

	target = [vort[i].xy for i in range(num_of_targets)]

	for i in range(num_of_targets):
		if vort[i].ele_type != "tracer":
			field[i][:] = vortex(vort[i], target)
	print field

	for i in range(num_of_targets):
		for j in range(num_of_vortex):
			if vort[i].fixed == 0:
				vort[i].updatexy = field[j][i]*dt + vort[i].updatexy

	target = [vort[i].updatexy for i in range(num_of_targets)]

	print target

	for i in range(num_of_targets):
		if vort[i].ele_type != "tracer":
			field2[i][:] = vortex(vort[i], target, "update")
	
	print field2

	for i in range(num_of_targets):
		for j in range(num_of_vortex):
			if vort[i].fixed == 0:
				vort[i].xy = (field[j][i]*dt/2) + (field2[j][i]*dt/2) + vort[i].xy
	print [i.xy for i in vort]

	for i in vort:
		i.update()

	print abs(vort[0].xy)
#	if (round(t/dt)%round(1/dt) == 0):
	X = [vort[i].xy.real for i in range(num_of_targets)]
	Y = [vort[i].xy.imag for i in range(num_of_targets)]

	line.set_xdata(X)
	line.set_ydata(Y)
	pylab.draw()
	

raw_input()

