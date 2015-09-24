from Plotting import PlotAll, plotInit
from simulation import *
from panelMethod import *
from diffusion import FetchControlPoints, NoSlipCondition, DiffuseBlobs, CheckReflection
from numpy import append

Elements = simulationInit()
#quiverElements = quiverPlot();
#numOfQE = len(quiverElements)

#Elements = append(quiverElements, Elements)

NumOfElements = len(Elements)

SimData = simulationParam()
Bound   = boundaryCondInit()

NumOfPanels = len(Bound)-1
Panels  = panelGeometry(NumOfPanels, Bound)
InvA = matInvAGen(Bound, Panels);

Graph = plotInit(SimData.Plotting, Elements)

X = []
Y = []

controlPoints = FetchControlPoints(Panels)
NumOfCP = len(controlPoints)

def numericalIntegration(allElements, Panels, dt):
	lenAllElements = len(allElements)

	FieldEuler = CalculateField(allElements, Panels)
	allElements = EulerPositionUpdate(allElements, FieldEuler, lenAllElements, dt)	
	b = matBGen(allElements, Panels, Bound)	#update b in midterms
	Panels = UpdatePanels(Panels, InvA, b);	#update strengths in midterms
	FieldRK2 = CalculateField(allElements, Panels)
	allElements = RKPositionUpdate(allElements, FieldRK2, FieldEuler, lenAllElements, dt)

	return allElements, FieldRK2, FieldEuler


def PanelUpdate(Elements, Panels, Bound, InvA):
	# Genrate b Matrix
	b = matBGen(Elements, Panels, Bound)

	# Update Panels with resp. strength
	Panels = UpdatePanels(Panels, InvA, b);	


	return Panels

for t in SimData.TimeStep:	
	
	NumOfElements = len(Elements)	

	#append CP with elements to treat CPs as Tracers
	allElements = append(Elements, controlPoints)  

	Panels = PanelUpdate(Elements, Panels, Bound, InvA)

	allElements, FieldRK2, FieldEuler = numericalIntegration(allElements, Panels, SimData.dt)

	# Remove appended CP with elements
	Elements = allElements[:NumOfElements]
	controlPoints = allElements[NumOfElements:]

	for i in Elements:
		i.updatexy = CheckReflection(0, 0, i.updatexy)

	#Update Locations of all the Elements
	[i.update() for i in Elements]


	PlotAll(Elements, Panels, FieldRK2, FieldEuler, Graph, X, Y, t, SimData.Plotting)

	print t


	# Generate Vortex Blobs to impose no slip condition
	vortexBlobs = NoSlipCondition(Bound, controlPoints, SimData.dt)

	# Diffuse blobs using random walk
	vortexBlobs = DiffuseBlobs(vortexBlobs, SimData.dt, Bound)

	# Append Blobs to the elements
	Elements = append(Elements, vortexBlobs)

	controlPoints = FetchControlPoints(Panels)

	PlotAll(Elements, Panels, FieldRK2, FieldEuler, Graph, X, Y, t, SimData.Plotting)
	print NumOfElements	


