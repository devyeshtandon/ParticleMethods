from pylab import arange
from elementDefinition import *
from geometryGenerate import *
from numpy import ones
def simulationInit():
	'''
        NumOfElements = 11
	
        Elements = [FluidElement() for i in range(NumOfElements)]
        delta = 0

        Elements[10] = Uniform(-10 - 0j)
        Elements[10].strength = 5

	tracerLocation = arange(-4.5,5.5,1)

	for i in range(10):
		Elements[i] = Tracer(-3 + tracerLocation[i]*1.0j)
	'''
	x = [0]
	y = [0]

        x = -2
        y = arange(-2, 2, 0.1)
	gridLength = 1

	NumOfElements = gridLength + 1
	
        Elements = [FluidElement() for i in range(NumOfElements)]

#for i in range(gridLength):

	Elements[0] = Vortex(-1.5 + 0j)
	Elements[0].strength = 5

	Elements[1] = Vortex(-2 + 0j)
#        Elements[NumOfElements-1] = Uniform(-10 - 0j)
	Elements[1].strength = 5
 #       Elements[NumOfElements-1].strength = 5

	return Elements

def boundaryCondInit():
	Z = UniformPolygon(40,1)
	return Z	

class simulationParam():
	dt       = 0.1
	SimTime  = 20
	TimeStep = arange(0, SimTime, dt)
	Plotting = 1
	SystemStatic  = 1
'''
Plotting
1 = Path Plot
2 = Quiver Plot
0 = Particles Motion Plot
'''

def EulerPositionUpdate(Elements, Field, NumOfElements, dt):	
	for i in range(NumOfElements):
		if (Elements[i].fixed == 0):
			for j in range(NumOfElements):
				Elements[i].xy += Field[j][i]*dt
	
	return Elements

def RKPositionUpdate(Elements, FieldRK, FieldEuler, NumOfElements, dt):	
	for i in range(NumOfElements):
		if (Elements[i].fixed == 0):
			for j in range(NumOfElements):
				Elements[i].updatexy += FieldRK[j][i]*dt/2 + FieldEuler[j][i]*dt/2 
	
	return Elements
