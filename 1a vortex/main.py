import numpy as np
import pylab
import math
import cmath
from elements import vortex

pi = math.pi

class elemental:
	xy       = 0;
	strength = 1;
	fixed    = 0;
	updatexy = xy;
	ele_type = "vortex"
	
	def location(self, x, *argv):
		if len(argv) == 1:
			self.xy = x + reduce((lambda y: y), argv)*1j
		else:
			self.xy = x
		self.updatexy = self.xy
	
	def update(self):
		self.updatexy = self.xy
	
############################################################################
# Counts
############################################################################

num_of_vortex    = 2
num_of_particles = 0
num_of_targets   = num_of_vortex + num_of_particles

############################################################################
# Elements Defined
############################################################################

vort = [elemental() for i in range(num_of_targets)]

vort[0].location(0.5,0)
vort[0].ele_type = "vortex"
vort[0].fixed = 0
vort[1].location(-0.5,0)

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

dt       = 0.1 ;
sim_time = 70;
time     = pylab.arange(0, sim_time, dt)

X = []
Y = []

alpha = 0.5

#############################################################################
# Simulation
#############################################################################
for t in time:	
	target = [vort[i].xy for i in range(num_of_vortex)]
	target.extend(part[i].xy for i in range(num_of_particles))

	for i in range(num_of_vortex):
		if vort[i].ele_type != "tracer":
			field[i][:] = vortex(vort[i], target)

	for i in range(num_of_targets):
		for j in range(num_of_targets):
			if vort[i].fixed == 0:
				vort[i].updatexy = field[j][i]*dt + vort[i].updatexy

	target = [vort[i].updatexy for i in range(num_of_vortex)]
	target.extend(part[i].updatexy for i in range(num_of_particles))

	for i in range(num_of_vortex):
		if vort[i].ele_type != "tracer":
			field2[i][:] = vortex(vort[i], target, "update")
	
	for i in range(len(vort)):
		for j in range(num_of_targets):
			if vort[i].fixed == 0:
				vort[i].xy = (field[j][i]*dt/2) + (field2[j][i]*dt/2) + vort[i].xy

	for i in vort:
		i.update()
	
	if (round(t/dt)%round(1/dt) == 0):
		X.extend(vort[i].xy.real for i in range(num_of_vortex))
		Y.extend(vort[i].xy.imag for i in range(num_of_vortex))

		line.set_xdata(X)
		line.set_ydata(Y)
		pylab.draw()

	print abs(vort[0].xy)
raw_input()

