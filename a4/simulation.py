from pylab import arange
from elementDefinition import *
from geometryGenerate import *

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

	'''
        x = arange(-2, 2.5, 0.5)
        y = arange(-2, 2.5, 0.5)
	gridLength = len(x)

	NumOfElements = gridLength**2 + 1
	
        Elements = [FluidElement() for i in range(NumOfElements)]

	for i in range(gridLength):
		for j in range(gridLength):
			Elements[i*gridLength + j] = Tracer(x[i] + y[j]*1.0j)
			Elements[i*gridLength + j].fixed = 0

        Elements[NumOfElements-1] = Uniform(-10 - 0j)
        Elements[NumOfElements-1].strength = 5
	'''

        NumOfElements = 1
        
        Elements = [FluidElement() for i in range(NumOfElements)]

        Elements[0] = Uniform(-10 - 0j)
        Elements[0].strength =1

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
	Z = UniformPolygon(41,1)
	return Z	

class simulationParam():
	dt       = 0.1
	SimTime  = 5
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
