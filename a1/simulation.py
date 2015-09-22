from pylab import arange
from elementDefinition import *

def simulationInit():
	NumOfElements = 2
	Elements = [FluidElement() for i in range(NumOfElements)]
	
	span = 1
	dx = span/NumOfElements
	
	locations   = arange(-0.5+dx/2, 0.5+dx/2, dx)
	for i in range(NumOfElements):
		Elements[i] = Vortex(locations[i]+0j)
	
	return Elements

class simulationParam():
	dt       = 0.1 ;
	SimTime  = 5;
	TimeStep = arange(0, SimTime, dt)
	PathPlot = 0

def EulerPositionUpdate(Elements, Field, NumOfElements, dt):	
	for i in range(NumOfElements):
		if (Elements[i].fixed == 0):
			for j in range(NumOfElements):
				Elements[i].xy += Field[i][j]*dt
	
	return Elements

def RKPositionUpdate(Elements, FieldRK, FieldEuler, NumOfElements, dt):	
	for i in range(NumOfElements):
		if (Elements[i].fixed == 0):
			for j in range(NumOfElements):
				Elements[i].updatexy += FieldRK[i][j]*dt/2 + FieldEuler[i][j]*dt/2 
	
	return Elements
