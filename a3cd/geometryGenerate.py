from math import pi
from math import cos
from math import sin




def UniformPolygon(NumOfSides, Radius):
	angleStep = 2.0*pi/NumOfSides
	angle = 0
	points = [0j for i in range(NumOfSides+1)]
	for i in range(NumOfSides):
		points[i] = Radius*(cos(angle) + 1.0j*sin(angle))
		angle += angleStep
	points[NumOfSides] = points[0]
	return points
