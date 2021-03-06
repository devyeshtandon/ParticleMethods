import numpy as np
from math import pi
from cmath import log
from cmath import exp
from math import sqrt
from math import atan2
from simulation import *

class FluidElement:
	xy       = 0;
	strength = 1;
	fixed    = 0;
	updatexy = xy;
	lastpos  = 0
	velocity = 0
	
	def update(self):
		self.xy = self.updatexy

	def updateLastPos(self):
		self.lastpos = self.xy
	
	def radDirection(self, target):
		if (self.xy == target):
			return 0;
		else:
			RelPosition = (target-self.xy)
			distance = abs(RelPosition)
			return RelPosition/distance

	def tanDirection(self, target):
		if (self.xy == target):
			return 0;
		else:
			RelPosition = (target-self.xy)
			distance = abs(RelPosition)
			return (-RelPosition.imag + RelPosition.real*1j)/distance
	
class Vortex(FluidElement):
	delta = 1e-3

	def __init__(self, loc):
		self.xy = loc
		self.updatexy = loc
		self.lastpos = loc

	def magnitude(self, target):
                if (self.xy == target):
                        return 0;
                else:
                        y = self.xy.imag
                        distance = abs(target-self.xy)
                        return self.strength*1.0*distance/2/pi/(distance**2 + self.delta**2)

	
	def fieldValue(self, target):
		if (self.xy == target):
			return 0;
		else:
			MagAtTarget = self.magnitude(target)
			DirAtTarget = self.tanDirection(target)
			return MagAtTarget*DirAtTarget

class Uniform(FluidElement):
	def __init__(self, loc):
		self.xy = loc
		self.updatexy = loc
		self.fixed = 1
		self.lastpos = loc

	def magnitude(self, target):
		return self.strength
	
	def fieldValue(self, target):
		MagAtTarget = self.magnitude(target)
		DirAtTarget = 1.0
		return MagAtTarget*DirAtTarget

class Tracer(FluidElement):
	def __init__(self, loc):
		self.xy = loc
		self.updatexy = loc
		self.strength = 0
		self.fixed = 0
		self.lastpos = loc

	def fieldValue(self, target):
		return 0


class VortexPanel(FluidElement):
	z1 = 0
	z2 = 0
	en = 0
	theta = 0
	length = 1;

	strength1 = 1
	strength2 = 1

	def __init__(self, loc1, loc2):
		self.z1 = loc1
		self.z2 = loc2
		relZ    = loc2-loc1
		self.en = (-relZ.imag + relZ.real*1j)/abs(relZ)
		self.theta = atan2(relZ.imag, relZ.real)
		self.length = abs(loc1-loc2)

	def matAValue(self, z):
		temp = (z-self.z1)*exp(-self.theta*1j)
		x = self.length/temp
		v1 = -1.0j/2/pi*((1.0/x - 1)*log(1-x) + 1)
		v1 = (v1.imag)
		v2 = 1.0j/2/pi*((1.0/x)*log(1-x) + 1)
		v2 = (v2.imag)
		return [v1, v2]

	def fieldValue(self, z):
		temp = (z-self.z1)*exp(-self.theta*1j)
		if temp == 0:
			return 0
		x = self.length/temp		
		v1 = np.conjugate(-1.0j/2/pi*((1.0/x - 1)*log(1-x) + 1))*exp(self.theta*1j)
		v2 = np.conjugate(1.0j/2/pi*((1.0/x)*log(1-x) + 1))*exp(self.theta*1j)

		return (v1*self.strength1 +  v2*self.strength2)

	def reinitialize(self):
		self.strength1 = 1
		self.strength2 = 1

def CalculateField(Elements, Panels):
        NumOfElements = len(Elements)
        Targets = [Elements[i].xy for i in range(NumOfElements)]

        for i in range(NumOfElements):
                if Elements[i].strength != 0:
                        for j in range(NumOfElements):
                                Elements[i].velocity += Elements[j].fieldValue(Elements[i].xy)

        NumOfPanels = len(Panels)
        for i in range(NumOfElements):
                for j in range(NumOfPanels):
                        Elements[i].velocity += (Panels[j].fieldValue(Elements[i].xy))

        return Elements

def CalculateFieldE(Elements):
        NumOfElements = len(Elements)
        Targets = [Elements[i].xy for i in range(NumOfElements)]

        for i in range(NumOfElements):
                if Elements[i].strength != 0:
                        for j in range(NumOfElements):
                                Elements[i].velocity += Elements[j].fieldValue(Elements[i].xy)
	return Elements
