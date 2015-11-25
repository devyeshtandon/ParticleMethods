from elementDefinition import FluidElement, Tracer, Vortex
from numpy import zeros, shape, random, append, sign, sqrt
from math import floor
from numpy import pi


def FetchControlPoints(Panel):
	numOfPanels = len(Panel)
	controlPoint = [FluidElement() for i  in range(numOfPanels)]
	
	for i in range(numOfPanels):
		temp = (Panel[i].z1 + Panel[i].z2)/2
		temp = temp + temp/abs(temp)*1.0e-6
		controlPoint[i] = Tracer(temp)
		controlPoint[i].fixed = 0

	return controlPoint

def NoSlipCondition(Boundary, controlPoints, dt):
	dim = len(controlPoints)
	
	lambdaLen = abs(Boundary[2]-Boundary[1])	
	deltaVal = lambdaLen/pi
	vortexBlob = [FluidElement() for i in range(dim)]
	for i in range(dim):
		vslip = (controlPoints[i].updatexy - controlPoints[i].lastpos)/dt
		mp = (Boundary[i+1] + Boundary[i])/2
		er = (Boundary[i+1] - Boundary[i])
		en = (er)/abs(er)
		gamma = (vslip.real*en.real + vslip.imag*en.imag)*lambdaLen
		vortexBlob[i] = Vortex(mp*(abs(mp)+deltaVal)/abs(mp))
		vortexBlob[i].strength = gamma
		vortexBlob[i].delta = deltaVal
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
	'''
	signum = (chkSign(bound1, bound2, 0))
	if ((chkSign(bound1, bound2, location)) == signum):
		location =  reflect(bound1, bound2, location)
	'''
	if (abs(location)<1):
		diff = 1-abs(location)
		location = location*(1+diff)/abs(location)

	return location
		

def DiffuseBlobs(vortexBlobs, time, boundary):
	lambdaLen = abs((boundary[2]-boundary[1]))

	mu = 1.12*1*2/1000
	sigma = sqrt(2*mu*time)
	numOfVortexBlobs = len(vortexBlobs)
	
	numOfDaughterBlobs = [0 for i in range(numOfVortexBlobs)]

	gammaMax = 0.1*lambdaLen

	for i in range(numOfVortexBlobs):
		temp = abs(vortexBlobs[i].strength)/gammaMax
		numOfDaughterBlobs[i] = int(floor(temp)) + 1

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

#		print vortexBlobs[i].strength
		if(vortexBlobs[i].strength>0):
			vortexBlobs[i].strength = vortexBlobs[i].strength - gammaMax*(numOfDaughterBlobs[i]-1)
			flag = 1
		else:
			vortexBlobs[i].strength = vortexBlobs[i].strength + gammaMax*(numOfDaughterBlobs[i]-1)
			flag = 0
#		print vortexBlobs[i].strength
#		print type(numOfDaughterBlobs[i])
		for j in range(numOfDaughterBlobs[i]-1): 
			locationTemp = vortexBlobs[i].xy + x[j] + y[j]
			locationTemp = CheckReflection(boundary[i], boundary[i+1], locationTemp)
			daughterBlobs[count] = Vortex(locationTemp)
			if flag == 1:
				daughterBlobs[count].strength = gammaMax
			else:
				daughterBlobs[count].strength = -gammaMax

			daughterBlobs[count].delta = vortexBlobs[i].delta
			count = count + 1
			

	vortexBlobs = append(vortexBlobs, daughterBlobs)

	return vortexBlobs

def cdCalculate(Elements):
	cd = 0
	for i in Elements:
		temp = i.xy
		cd += i.strength*(temp.imag -1.0j*temp.real)

	return cd
	
