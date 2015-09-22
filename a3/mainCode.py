from Plotting import *
from simulation import *
from panelMethod import *

Elements = simulationInit()
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

for t in SimData.TimeStep:	
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
	if SimData.PathPlot == 1:
		plotPathLine(Elements, Panels, Graph, X, Y);
	else:
		plotParticles(Elements, Panels, Graph);
#	print abs(Elements[0].xy)
#	raw_input()
raw_input()

