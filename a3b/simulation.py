from pylab import arange
from elementDefinition import *
from geometryGenerate import *

def simulationInit(delta):
        NumOfElements = 251
        Elements = [FluidElement() for i in range(NumOfElements)]
        locations = UniformPolygon(250, 1+delta)
        for i in range(250):
                Elements[i] = Tracer(locations[i])
        Elements[250] = Uniform(-125 - 0j)
        Elements[250].strength = 15

	return Elements

def boundaryCondInit():
	Z = UniformPolygon(100,1)
	return Z	

class simulationParam():
	dt       = 0.01
	SimTime  = 5
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
		Elements[i].updatexy = 0
		if (Elements[i].fixed == 0):
			for j in range(NumOfElements):
				Elements[i].updatexy += FieldRK[j][i]*dt/2 + FieldEuler[j][i]*dt/2 
	
	return Elements
