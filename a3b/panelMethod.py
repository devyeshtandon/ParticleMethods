from elementDefinition import *
import cmath
import numpy as np

def panelGeometry(NoOfPanels, geometry):
	Panels = [FluidElement() for i in range(NoOfPanels)]

	for i in range(NoOfPanels):
		Panels[i] = VortexPanel(geometry[i], geometry[i+1]) 
	return Panels

# Matrix A formation
def matInvAGen(geometry, Panels):
	GeoLen = len(geometry)
	MidPts = [1.0*(geometry[i] + geometry[i+1])/2 for i in range(GeoLen-1)]

	ArrSize	 = len(MidPts)
	A = np.zeros(shape = (ArrSize+1, ArrSize), dtype = complex)

	for i in range(ArrSize):
		for j in range(ArrSize):	
			try:
				A[i,j:j+2] += Panels[j].matAValue(MidPts[i])
			except:
				temp = Panels[j].matAValue(MidPts[i])
				A[i,0] += temp[1]
				A[i,j] += temp[0]

	A[ArrSize,:] = 1
#	print A
	invA = np.linalg.pinv(A)
#	print invA
	return invA

def matBGen(Elements, Panels, geometry):
	GeoLen = len(geometry)
	MidPts = [1.0*(geometry[i] + geometry[i+1])/2 for i in range(GeoLen-1)]
	
	ArrSize = len(MidPts)
	b = np.zeros(shape = (ArrSize+1, 1), dtype = complex)
	for j in range(ArrSize):
		for i in range(len(Elements)):
			b[j,0] += Elements[i].fieldValue(MidPts[j])
	for j in range(len(MidPts)):
		b[j, 0] = b[j,0].real*Panels[j].en.real + b[j,0].imag*Panels[j].en.imag
	b[ArrSize,:] = 0

	return b	

def UpdatePanels(Panels, InvA, b):
	X = np.dot(InvA, b)
#	print 'b'
#	print X
#	print 'yo'
	for i in range(len(Panels)):
		try:
			Panels[i].strength1 = X[i,0]
			Panels[i].strength2 = X[i+1,0]
		except:
			Panels[i].strength1 = X[i,0]
			Panels[i].strength2 = X[0,0]

	return Panels

