from pylab import arange
from elementDefinition import *
from geometryGenerate import *
from math import pi

def simulationInit(x):
        NumOfElements = 252
        Elements = [FluidElement() for i in range(NumOfElements)]
        delta = x
        locations = UniformPolygon(250, 1+delta)
        for i in range(250):
                Elements[i] = Tracer(locations[i])
        Elements[250] = Uniform(-125 - 0j)
        Elements[250].strength = 5
	Elements[251] = Doublet(0.0-0j)
	Elements[251].fixed = 1
	Elements[251].strength = 10*2*pi
	
	return Elements

class simulationParam():
	dt       = 0.01
	SimTime  = 5
	TimeStep = arange(0, SimTime, dt)
	PathPlot = 1

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
