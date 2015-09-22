from pylab import arange
from elementDefinition import *
from geometryGenerate import *

def simulationInit():
        NumOfElements = 1
        Elements = [FluidElement() for i in range(NumOfElements)]
 #       delta = 0.01
#        locations = UniformPolygon(250, 1+delta)
 #       for i in range(250):
#                Elements[i] = Tracer(locations[i])
        Elements[0] = Vortex(-1.25 - 0j)
        Elements[0].strength = 5

	return Elements

def boundaryCondInit():
	Z = UniformPolygon(3,1)
	return Z	

class simulationParam():
	dt       = 0.1
	SimTime  = 50
	TimeStep = arange(0, SimTime, dt)
	PathPlot = 1
	SystemStatic  = 1

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
