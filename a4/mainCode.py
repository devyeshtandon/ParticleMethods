from Plotting import *
from simulation import *
from panelMethod import *
from diffusion import FetchControlPoints, NoSlipCondition, DiffuseBlobs
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

if SimData.Plotting == 1:
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

	if (SimData.SystemStatic == 0):
		Panels  = panelGeometry(len(Bound))
		InvA = matInvAGen(Bound, Panels)
	
####### ADVECTION ############################################################################
	
	NumOfElements = len(Elements)	

	#append CP with elements to treat CPs as Tracers
	allElements = append(Elements, controlPoints)  

	Panels = PanelUpdate(Elements, Panels, Bound, InvA)
	allElements, FieldRK2, FieldEuler = numericalIntegration(allElements, Panels, SimData.dt)



	# Remove appended CP with elements
	Elements = allElements[:NumOfElements]
	controlPoints = allElements[NumOfElements:]

	#Update Locations of all the Elements
	[i.update() for i in Elements]

####### DIFFUSION  ##########################################################################
	
	# Generate Vortex Blobs to impose no slip condition
	vortexBlobs = NoSlipCondition(Bound, controlPoints, NumOfCP, SimData.dt)

	# Diffuse blobs using random walk
	vortexBlobs = DiffuseBlobs(vortexBlobs, SimData.dt, Bound)

	# Append Blobs to the elements
	Elements = append(Elements, vortexBlobs)

####### PLOTTING ###########################################################################
	controlPoints = FetchControlPoints(Panels)

	if SimData.Plotting == 1:
		plotPathLine(Elements, Panels, Graph, X, Y)
	elif SimData.Plotting == 0:
		plotParticles(Elements, Panels, Graph)
	elif SimData.Plotting == 2:
		plotQuiver(FieldRK2, FieldEuler, Graph, numOfQE, NumOfElements, Panels)

	print NumOfElements	
	raw_input()


