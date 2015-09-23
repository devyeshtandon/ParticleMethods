from Plotting import *
from simulation import *
from panelMethod import *

Elements = simulationInit()
NumOfElements = len(Elements)

SimData = simulationParam()
Bound   = boundaryCondInit()

NumOfPanels = len(Bound)-1
Panels  = panelGeometry(NumOfPanels, Bound)
A = matInvAGen(Bound, Panels);

Graph = plotInit(SimData.Plotting, Elements)

if SimData.Plotting == 1:
	X = []
	Y = []

#controlPoints = FetchControlPoints(Panels)
#NumOfCP = len(controlPoints)

for t in SimData.TimeStep:	
# Advection
	if (SimData.SystemStatic == 0):
		Panels  = panelGeometry(len(Bound))
		A = matInvAGen(Bound, Panels)
	
	b = matBGen(Elements, Panels, Bound)	

	Panels = UpdatePanels(Panels, A, b);	

	FieldEuler = CalculateField(Elements, Panels)
	Elements = EulerPositionUpdate(Elements, FieldEuler, NumOfElements, SimData.dt)
	b = matBGen(Elements, Panels, Bound)	

	Panels = UpdatePanels(Panels, A, b);	

	FieldRK2 = CalculateField(Elements, Panels)
	Elements = RKPositionUpdate(Elements, FieldRK2, FieldEuler, NumOfElements, SimData.dt)

	[i.update() for i in Elements]

# Diffusion
#	slipVelocities = CalculateVSlip(Panels)

#	print FieldEuler
#	print FieldRK2

	if SimData.Plotting == 1:
		plotPathLine(Elements, Panels, Graph, X, Y)
	elif SimData.Plotting == 0:
		plotParticles(Elements, Panels, Graph)
	elif SimData.Plotting == 2:
		NumOfTracers = NumOfElements-1
		plotQuiver(FieldRK2, FieldEuler, Graph, NumOfTracers, Panels)
		

	raw_input()


