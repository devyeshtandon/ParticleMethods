from numpy import linspace, sin, pi, cos

import matplotlib.pyplot as plt

from interpolate import interpolate1D

def assignment1(x, fnVal, baseSize, kernal):


	[interpX, interpFn] = interpolate1D(x, fnVal, baseSize, var, kernal)
	
	return [interpX, interpFn]
	
if __name__ == '__main__':
	x = linspace(-1,1,40)
	fnVal = sin(pi*x)
	dfnVal = pi*cos(pi*x)
	baseSize = 300

	var = 1.05*0.05;

	[X, Y] = assignment1(x, fnVal, baseSize, 'GS')
	[Xd, Yd] = assignment1(x, fnVal, baseSize, 'DGS')
	plt.subplot(2,1,1)
	plt.plot(X, Y)
	plt.plot(x, fnVal, 'ro')
	plt.title('Interpolation of fn and its derivative using Gaussian')
	
	plt.subplot(2,1,2)
	plt.plot(Xd, Yd)
	plt.plot(x, dfnVal, 'ro')
	
	plt.show()


