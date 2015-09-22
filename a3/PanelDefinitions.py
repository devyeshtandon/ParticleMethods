from math import atan2

class PanelSheet():
	z1 = 0
	z2 = 0
	en = 0
	theta = 0

	strength1 = 1
	strength2 = 1

	def __init__(self, loc1, loc2):
		self.z1 = loc1
		self.z2 = loc2
		relZ    = loc2-loc1
		self.en = (-relZ.imag + relZ.real*1j)/abs(relZ)
		self.theta = atan2(relZ.imag, relZ.real)

	def velocity(self, z):
		
