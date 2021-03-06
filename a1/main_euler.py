import numpy as np
import pylab
import math
import cmath
from elements import vortex

pi = math.pi

class elemental:
	xy       = 0;
	strength = 3;
	fixed    = 0;
	updatexy = xy;
	ele_type = "uniform"
	
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

vort[0].location(-0.5, 0)
vort[0].fixed =0 
vort[0].strength = 1
vort[0].ele_type = "vortex"
vort[1].location(0.5, 0)
vort[1].strength = 1
vort[1].fixed = 0
vort[1].ele_type = "vortex"

for i in pylab.arange(num_of_vortex, num_of_targets, 1):
	vort[i].ele_type = "tracer"
	
#vort[2].location(-0, 0.0)
#vort[4].location(-0, 0.4)
#vort[6].location(-0, 0.8)
#vort[8].location(-0, 1.2)
#vort[10].location(-0,1.6)
#vort[3].location(-0, -0.4)
#vort[5].location(-0, -0.8)
#vort[7].location(-0, -1.2)
#vort[9].location(-0, -1.6)
#vort[11].location(-0,-2)

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
	target = [vort[i].xy for i in range(num_of_targets)]

	for i in range(num_of_targets):
		if vort[i].ele_type != "tracer":
			field[i][:] = vortex(vort[i], target)

	for i in range(num_of_targets):
		for j in range(num_of_vortex):
			if vort[i].fixed == 0:
				vort[i].xy = field[j][i]*dt + vort[i].xy
	
#	if (round(t/dt)%round(1/dt) == 0):
	X.extend(vort[i].xy.real for i in range(num_of_targets))
	Y.extend(vort[i].xy.imag for i in range(num_of_targets))

	line.set_xdata(X)
	line.set_ydata(Y)
	pylab.draw()

raw_input()

