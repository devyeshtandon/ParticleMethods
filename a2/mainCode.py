from Plotting import *
from simulation import *
from cmath import exp
from math import atan2
from numpy import zeros

def del2(x):
	Elements = simulationInit(x)
	NumOfElements = len(Elements)

	SimData = simulationParam()

	Graph = plotInit()

	def reflection(point):
	        temp = point/(abs(point)**2)
        	return temp

	if SimData.PathPlot == 1:
		X = []
		Y = []

	X = zeros(shape=(250,1))
#for t in SimData.TimeStep:	
	Elements[1].xy = reflection(Elements[2].xy)
	Elements[1].updatexy = reflection(Elements[2].updatexy)
	Elements[1].strength = -Elements[2].strength/abs(Elements[1].xy)
	Elements[0].strength = -Elements[1].strength
	
	FieldEuler = CalculateField(Elements, NumOfElements)
	Elements = EulerPositionUpdate(Elements, FieldEuler, NumOfElements, SimData.dt)
	Elements[1].xy = reflection(Elements[2].xy)
	Elements[1].updatexy = reflection(Elements[2].updatexy)
	Elements[1].strength = -Elements[2].strength
	Elements[0].strength = -Elements[1].strength

	FieldRK2 = CalculateField(Elements, NumOfElements)
	Elements = RKPositionUpdate(Elements, FieldRK2, FieldEuler, NumOfElements, SimData.dt)

	[i.update() for i in Elements]

#	if SimData.PathPlot == 1:
#		plotPathLine(Elements, Graph, X, Y);
#	else:
#		plotParticles(Elements, Graph);
	for i in range(250):
		X[i] = abs(Elements[i].xy)


	return X
