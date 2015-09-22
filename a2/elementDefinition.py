from math import pi
from math import sqrt
from simulation import *

class FluidElement:
	xy       = 0;
	strength = 1;
	fixed    = 0;
	updatexy = xy;
	
	def update(self):
		self.xy = self.updatexy
	
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
	def __init__(self, loc):
		self.xy = loc
		self.updatexy = loc

	def magnitude(self, target):
		if (self.xy == target):
			return 0;
		else:
			NumOfElemets = 90
			y = self.xy.imag
			self.strength = 10.0
			distance = abs(target-self.xy)
			BlobSize = 1
			return self.strength*1.0*distance/2/pi/(distance**2 + BlobSize**2)
	
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

        def fieldValue(self, target):
                return 0

class Doublet(FluidElement):
	def __init__(self, loc):
                self.xy = loc
                self.updatexy = loc
                self.fixed =11

        def fieldValue(self, target):
		if (self.xy ==target):
			return 0
		else:
			distance = abs(self.xy - target)
			magnitude = self.strength*1.0/2/pi/(distance**2)
			tangValue = -(magnitude*target.imag/distance)
			radValue = -(magnitude*target.real/distance)
			tangField = tangValue*self.tanDirection(target)
			radField = radValue*self.radDirection(target)
                return (tangField + radField)
 

def CalculateField(Elements, NumOfElements):
	Targets = [Elements[i].xy for i in range(NumOfElements)]
	Field = [[0 for x in range(NumOfElements)] for x in range(NumOfElements)]

	for i in range(NumOfElements):
		if Elements[i].strength != 0:
			Field[i][:] = [Elements[i].fieldValue(j) for j in Targets]
	return Field

