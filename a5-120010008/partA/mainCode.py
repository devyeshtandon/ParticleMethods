#from Plotting import PlotAll, plotInit
from simulation import *
from panelMethod import *
from diffusion import FetchControlPoints, NoSlipCondition, DiffuseBlobs, CheckReflection, cdCalculate
from numpy import append, savetxt
from SavingData import SaveData

Elements = simulationInit()

quiverElements = quiverPlot()
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
controlPoints = []
NumOfCP = len(controlPoints)

def numericalIntegration(allElements, Panels, dt):
	lenAllElements = len(allElements)

	allElements = CalculateFieldE(allElements, Panels)
	FieldEuler = [i.velocity for i in allElements]

	allElements = EulerPositionUpdate(allElements, lenAllElements, dt)	
	b = matBGen(allElements, Panels, Bound)	#update b in midterms
	Panels = UpdatePanels(Panels, InvA, b);	#update strengths in midterms

	allElements = CalculateFieldE(allElements, Panels)
	allElements = RKPositionUpdate(allElements, FieldEuler, lenAllElements, dt)
	
	return allElements


def PanelUpdate(Elements, Panels, Bound, InvA):
	# Genrate b Matrix
	b = matBGen(Elements, Panels, Bound)

	# Update Panels with resp. strength
	Panels = UpdatePanels(Panels, InvA, b);	
	return Panels

cd = []
for t in SimData.TimeStep:		

	NumOfElements = len(Elements)	
	allElements = append(Elements, controlPoints)  
	Panels = PanelUpdate(Elements, Panels, Bound, InvA)
	allElements = numericalIntegration(allElements, Panels, SimData.dt)

	# Remove appended CP with elements
	Elements = allElements[:NumOfElements]
	controlPoints = allElements[NumOfElements:]

	#Update Locations of all the Elements
	[i.update() for i in Elements]

	# Generate Vortex Blobs to impose no slip condition
	vortexBlobs = NoSlipCondition(Bound, controlPoints, SimData.dt)

	# Diffuse blobs using random walk
	vortexBlobs = DiffuseBlobs(vortexBlobs, SimData.dt, Bound)

	# Append Blobs to the elements
	Elements = append(Elements, vortexBlobs)
	controlPoints = FetchControlPoints(Panels)
	SaveData(Elements, t, numOfQE)
	raw_input()
	
	
	
savetxt('cdplot.txt', cd)
