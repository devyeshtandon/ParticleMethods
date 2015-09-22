from elementDefinition import FluidElement, Tracer, Vortex
from numpy import zeros, shape, random, append, sign, sqrt
from math import floor
from numpy import pi


def FetchControlPoints(Panel):
	numOfPanels = len(Panel)
	controlPoint = [FluidElement() for i  in range(numOfPanels)]
	
	for i in range(numOfPanels):
		temp = (Panel[i].z1 + Panel[i].z2)/2
		temp = temp/abs(temp)*1.01
		controlPoint[i] = Tracer(temp)
		controlPoint[i].fixed = 1

	return controlPoint

def NoSlipCondition(Boundary, field1, field2, length):
	dim = shape(field1)

	dim =  dim[0]
	
	lambdaLen = abs(Boundary[2]-Boundary[1])	
	deltaVal = lambdaLen/pi

	vortexBlob = [FluidElement() for i in range(length)]
	for i in range(dim-length, dim):
		vslip = 0
		counter = i-dim+length
                for j in range(dim):
			vslip += (field1[j][i] + field2[j][i])/2
		mp = (Boundary[counter+1] + Boundary[counter])/2
		er = (Boundary[counter+1] - Boundary[counter])
		en = (er)/abs(er)
		gamma = (vslip.real*en.real + vslip.imag*en.imag)*lambdaLen
		vortexBlob[counter] = Vortex(mp*(abs(mp)+deltaVal)/abs(mp))
		vortexBlob[counter].strength = gamma
		vortexBlob[counter].delta = deltaVal

	return vortexBlob

def reflect(p1, p2, X):
	x1 = p1.real
	y1 = p1.imag

	x2 = p2.real
	y2 = p2.imag

	if(x1==x2):
		Xp = 2*x1 - X.real + X.imag*1.0j
		return Xp

	m = ((y2-y1)/(x2-x1))

	c = (y1 - x1*m)
	
	x = X.real
	y = X.imag

	d = (x + m*(y-c))/(1+m**2)
	
	Xp = (2*d - x) + (2*d*m - y + 2*c)*1j
	return Xp

def chkSign(p1, p2, X): ### Assume only even partitions else x1 = x2
	x1 = p1.real
	y1 = p1.imag

	x2 = p2.real
	y2 = p2.imag

	m = ((y2-y1)/(x2-x1))
	c = (y1 - x1*m)
	
	x = X.real
	y = X.imag
	
	return sign(y-m*x-c)

def CheckReflection(bound1, bound2, location):
	signum = (chkSign(bound1, bound2, 0))
	if ((chkSign(bound1, bound2, location)) == signum):
		location =  reflect(bound1, bound2, location)
	return location
		

def DiffuseBlobs(vortexBlobs, time, boundary):
	
	mu = 1.12*1*2/1000
	sigma = sqrt(2*mu*time)
	numOfVortexBlobs = len(vortexBlobs)
	
	numOfDaughterBlobs = zeros(numOfVortexBlobs)

	gammaMax = 0.1

	for i in range(numOfVortexBlobs):
		temp = abs(vortexBlobs[i].strength)/gammaMax 
		numOfDaughterBlobs[i] = (floor(temp)) + 1

	newNumDaughterBlobs = int(sum(numOfDaughterBlobs) - numOfVortexBlobs)	
	daughterBlobs = [FluidElement() for i in range(newNumDaughterBlobs)]

	count = 0

	for i in range(numOfVortexBlobs):
		try:
			x = random.normal(0, sigma, numOfDaughterBlobs[i])
			y = random.normal(0, sigma, numOfDaughterBlobs[i])*1.0j
		except:
			x = 0
			y = 0
		vortexBlobs[i].strength = vortexBlobs[i].strength/int(numOfDaughterBlobs[i])

		for j in range(int(numOfDaughterBlobs[i]-1)): 
			locationTemp = vortexBlobs[i].xy + x[j] + y[j]
			locationTemp = CheckReflection(boundary[i], boundary[i+1], locationTemp)
			daughterBlobs[count] = Vortex(locationTemp)
			daughterBlobs[count].strength = vortexBlobs[i].strength
			daughterBlobs[count].delta = vortexBlobs[i].delta
			count = count + 1
			

	vortexBlobs = append(vortexBlobs, daughterBlobs)

	return vortexBlobs
	
