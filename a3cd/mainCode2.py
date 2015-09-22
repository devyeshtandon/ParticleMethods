from Plotting import *
from simulation import *
from panelMethod import *
from numpy import zeros

def delta2(x):
	Elements = simulationInit(x)
	NumOfElements = len(Elements)

	SimData = simulationParam()
	Bound   = boundaryCondInit()

	NumOfPanels = len(Bound)-1
	Panels  = panelGeometry(NumOfPanels, Bound)
	InvA = matInvAGen(Bound, Panels);

	Graph = plotInit()

	if SimData.PathPlot == 1:
		X = []
		Y = []
	X = zeros(shape=(250,1))
#for t in SimData.TimeStep:	
	if (SimData.SystemStatic == 0):
		Panels  = panelGeometry(len(Bound))
		InvA = matInvAGen(Bound, Panels)
	
	b = matBGen(Elements, Panels, Bound)	

	Panels = UpdatePanels(Panels, InvA, b);	

	FieldEuler = CalculateField(Elements, Panels)
	Elements = EulerPositionUpdate(Elements, FieldEuler, NumOfElements, SimData.dt)
	b = matBGen(Elements, Panels, Bound)	

	Panels = UpdatePanels(Panels, InvA, b);	

	FieldRK2 = CalculateField(Elements, Panels)
	Elements = RKPositionUpdate(Elements, FieldRK2, FieldEuler, NumOfElements, SimData.dt)

#	print FieldRK2

	[i.update() for i in Elements]

#	print Elements[0].xy
#	if SimData.PathPlot == 1:
#		plotPathLine(Elements, Panels, Graph, X, Y);
#	else:
#		plotParticles(Elements, Panels, Graph);
	for i in range(250):
		X[i] =  abs(Elements[i].updatexy)

	return X
