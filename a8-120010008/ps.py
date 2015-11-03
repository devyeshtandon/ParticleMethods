from  numpy import arange, zeros, concatenate, ones, sqrt
from kernalDefinitions import CubicSpline1D, DerCubicSpline1D
import matplotlib.pyplot as plt

class Particle():
	p = 0.0
	u = 0.0
	rho = 0.0
	m = 0.0
	x = 0.0

	def init(self, p, u, rho, m, x):
		self.p = p
		self.u = u
		self.rho = rho
		self.m = m
		self.x = x
		self.e = p/0.4/rho
		return self
	
	def updateP(self):
		self.p = self.e*self.rho*(0.4)
		return self

def initialize():
        xl = arange(-1.125, 0, 0.0015625)
        xr = arange(0 ,3.0, 0.00625)
        x = concatenate((xl, xr), 1)


	Pa = [Particle() for i in x]
	for i in range(len(x)):
		if x[i]<0:
			Pa[i] = Pa[i].init(1., .0, 1.0, 0.0015625, x[i])
                else:
			Pa[i] = Pa[i].init(0.1, 0.0, 0.250, 0.0015625, x[i])

	h = 2*0.00625

	return [Pa, h]

def cVis(P1, P2, h):
	vab = P1.u - P2.u
	xab = P1.x - P2.x
	eta = 0.00001;
	gmm = 1.4

	mu = h*vab*xab/(xab**2 + eta**2)

	ca = sqrt(P1.p/P1.rho*gmm)
	cb = sqrt(P2.p/P2.rho*gmm)
	cab= (ca + cb)/2

	pi = 2.0*(-cab*mu + mu**2)/(P1.rho + P2.rho)

	return pi

def binning(Pa, h):
	minDis = 0.0015625;
	for i in range(400,800):
		if(minDis>(Pa[i+1].x-Pa[i].x)):
			minDis = (Pa[i+1].x-Pa[i].x)

	a = 2.0*h/minDis
#	return int(round(a)+1)
	return ;	


def propogate(Pa, h, dt):

	numPa = len(Pa)/3

	sumd = zeros(numPa);
	sumv = zeros(numPa);
	sume = zeros(numPa)
	xsph = zeros(numPa);

	sR = binning(Pa, h);

	for i in range(len(Pa)/3):
		a = i+numPa
		Wab = Pa[a].x - Pa[a-sR].x 
		temp = CubicSpline1D(h, float(Wab))	
		assert(temp <0.001)
		for j in range(-sR,sR):
			Wab = Pa[a].x - Pa[a+j].x 
			temp = CubicSpline1D(h, float(Wab))	
			tempd = DerCubicSpline1D(h, float(Wab))
#			print tempd
			if ((Pa[a].u - Pa[a+j].u)*Wab)<0:
				piab = cVis(Pa[a], Pa[a+j], h)
			else:
				piab = 0;

			sumd[i] += Pa[a+j].m*temp

			J = Pa[a+j].m*((Pa[a].p/(Pa[a].rho**2)) + (Pa[a+j].p/(Pa[a+j].rho**2)) + piab)*tempd

			sumv[i] += -J
			sume[i] += 0.5*J*(Pa[a].u-Pa[a+j].u)

			xsph[i] += Pa[a+j].m*((-Pa[a].u + Pa[a+j].u)/(Pa[a].rho + Pa[a+j].rho))*temp
#		raw_input()
	
	for i in range(numPa):
		Pa[i+numPa].rho = sumd[i]
		Pa[i+numPa].e += sume[i]*dt
		Pa[i+numPa].x += Pa[i+numPa].u*dt + 0.5*sumv[i]*dt*dt + xsph[i]*dt;
		Pa[i+numPa].u += sumv[i]*dt
		Pa[i+numPa] = Pa[i+numPa].updateP()

#	[plt, x] = plotGraph(Pa);
#	plt.plot(x[400:800], sumv+xsph)
#	plt.show()	
	return [Pa, h]


def plotGraph(Pa):
	x = zeros(len(Pa))
	y = zeros(len(Pa))
	for i in range(len(Pa)):
		y[i] = Pa[i].rho
		x[i] = Pa[i].x

	plt.plot(x, y)

	return [plt, x]

