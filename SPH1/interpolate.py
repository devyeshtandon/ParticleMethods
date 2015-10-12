from copy import copy
from numpy import linspace, zeros, arange, random
from kernalDefinitions import Gaussian1D, CubicSpline1D, DerCubicSpline1D, DerGaussian1D
from numpy import pi, sin

def interpolate1D(x, fnVal, baseSize, var, kernal):
	numOfX = len(x)
	interpX = linspace(min(x), max(x), baseSize)
	interpFn = zeros(len(interpX))

	tempX = linspace(3.0*min(x), 3.0*max(x), 3*numOfX-2)
	fnValN = sin(2*pi*tempX) + random.random(len(tempX))

	for i in range(len(interpX)):
		for j in arange(len(tempX)):
			q = (interpX[i] - tempX[j])/var
			if kernal == 'GS':
				temp = Gaussian1D(var, q)
			elif kernal == 'CS':
				temp = CubicSpline1D(var, q)
			elif kernal == 'DGS':
				temp = DerGaussian1D(var, q)
			elif kernal == 'DCS':
				temp = DerCubicSpline1D(var, q)
			interpFn[i] += temp*fnValN[j]*0.05

	return [interpX, interpFn]
