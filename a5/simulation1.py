from numpy import arange
from elementDefinition import *
from geometryGenerate import *
import random

def simulationInit():

        NumOfElements = 2000
        x = [random.uniform(-2,2) for i in range(NumOfElements)]
        y = [random.uniform(-2,2) for i in range(NumOfElements)]
        Elements = [FluidElement() for i in range(NumOfElements)]

	for i in range(NumOfElements):
	        Elements[i] = Vortex(complex(x[i],y[i]))
        	Elements[i].strength = 1

	return Elements

def quiverPlot():
        x = arange(-2, 2, 0.2)
        y = arange(-2, 2, 0.2)
        gridLength = len(x)

        NumOfElements = gridLength**2
        
        Elements = [FluidElement() for i in range(NumOfElements)]

        for i in range(gridLength):
                for j in range(gridLength):
                        Elements[i*gridLength + j] = Tracer(x[i] + y[j]*1.0j)
                        Elements[i*gridLength + j].fixed = 0
	return Elements

def boundaryCondInit():
	Z = UniformPolygon(40,1)
	return Z	

class simulationParam():
	dt       = 0.1
	SimTime  = 3
	TimeStep = arange(0, SimTime, dt)
	Plotting = 0
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
