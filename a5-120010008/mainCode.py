#from Plotting import PlotAll, plotInit
from simulation import *
from panelMethod import *
from diffusion import FetchControlPoints, NoSlipCondition, DiffuseBlobs, CheckReflection, cdCalculate
from numpy import append, savetxt
from SavingData import SaveData
from node import NodeMain

Elements = simulationInit()

quiverElements = quiverPlot();
numOfQE = len(quiverElements)
Elements = append(quiverElements, Elements)

NumOfElements = len(Elements)

SimData = simulationParam()
Bound   = boundaryCondInit()

NumOfPanels = len(Bound)-1
Panels  = panelGeometry(NumOfPanels, Bound)
InvA = matInvAGen(Bound, Panels);

#Graph = plotInit(SimData.Plotting, Elements)

X = []
Y = []

controlPoints = FetchControlPoints(Panels)
NumOfCP = len(controlPoints)

def numericalIntegration(allElements, Panels, dt):
	lenAllElements = len(allElements)
	
	temp = allElements
	allElements = NodeMain(allElements)
	for i in allElements:
		i.velocity += 1.0 + 0j
	allElements = CalculateFieldP(allElements, Panels)
	
	temp = CalculateField(temp, Panels)
	for i in range(len(temp)):
		assert(abs(temp[i].velocity - allElements[i].velocity)<0.1)
#		print allElements[i].velocity
#	raw_input()

	allElements = EulerPositionUpdate(allElements, 0, lenAllElements, dt)	
	FieldEuler = [i.velocity for i in allElements]
	b = matBGen(allElements, Panels, Bound)	
	Panels = UpdatePanels(Panels, InvA, b)

	allElements = NodeMain(allElements)
	for i in allElements:
		i.velocity += 1. + 0.j

	allElements = CalculateFieldP(allElements, Panels)

	allElements = RKPositionUpdate(allElements, 0, FieldEuler, lenAllElements, dt)

	return allElements, 0, FieldEuler


def PanelUpdate(Elements, Panels, Bound, InvA):
	# Genrate b Matrix
	b = matBGen(Elements, Panels, Bound)

	# Update Panels with resp. strength
	Panels = UpdatePanels(Panels, InvA, b);	


	return Panels

cd = []
for t in SimData.TimeStep:	
	
	NumOfElements = len(Elements)	

	#append CP with elements to treat CPs as Tracers
	allElements = append(Elements, controlPoints)  

	Panels = PanelUpdate(Elements, Panels, Bound, InvA)

	allElements, FieldRK2, FieldEuler = numericalIntegration(allElements, Panels, SimData.dt)

	# Remove appended CP with elements
	Elements = allElements[:NumOfElements]
	controlPoints = allElements[NumOfElements:]

	for i in range(numOfQE, NumOfElements):
		Elements[i].updatexy = CheckReflection(0, 0, Elements[i].updatexy)

	#Update Locations of all the Elements
	[i.update() for i in Elements]

    
#	PlotAll(Elements, Panels, FieldRK2, FieldEuler, Graph, X, Y, t, SimData.Plotting)

	print t

	# Generate Vortex Blobs to impose no slip condition
	vortexBlobs = NoSlipCondition(Bound, controlPoints, SimData.dt)

	# Diffuse blobs using random walk
	vortexBlobs = DiffuseBlobs(vortexBlobs, SimData.dt, Bound)

	# Append Blobs to the elements
	Elements = append(Elements, vortexBlobs)

	controlPoints = FetchControlPoints(Panels)

#	PlotAll(Elements, Panels, FieldRK2, FieldEuler, Graph, X, Y, t, SimData.Plotting)
	
	SaveData(Elements, t, numOfQE)

#	Elements[:numOfQE] = quiverPlot()

#	cd = append(cd, cdCalculate(Elements[1:]))
#	print cd
#	raw_input()
	
	
	
savetxt('cdplot.txt', cd)
