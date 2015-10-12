from numpy import linspace, sin, pi, cos, linalg, zeros, random

import matplotlib.pyplot as plt

from interpolate import interpolate1D

def assignment1(x, fnVal, baseSize, kernal):


	[interpX, interpFn] = interpolate1D(x, fnVal, baseSize, var, kernal)
	
	return [interpX, interpFn]
	
if __name__ == '__main__':
	x = linspace(-1,1,40)
	fnVal = sin(2*pi*x) + random.random(len(x))
	dfnVal = 2*pi*cos(2*pi*x)
	baseSize = 200
	
	h = [ 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4] 
	count = 0
	e = zeros(len(h))
	p = zeros(len(h))

	nx = linspace(-1,1,200)
	fnX = sin(2*pi*nx)
	dfnX = 2*pi*cos(2*pi*nx)
	for i in h:
		var = i*0.05;

		[X, Y] = assignment1(x, fnVal, baseSize, 'GS')
		[Xd, Yd] = assignment1(x, fnVal, baseSize, 'DGS')
		e[count] = linalg.norm(fnX - Y)
		p[count] = linalg.norm(dfnX - Yd)
		count = count + 1

	plt.subplot(2,1,1)
	plt.plot(h, e, 'o')
	plt.title('L2 Error at different h')
	
	plt.subplot(2,1,2)
	plt.plot(h, p, 'ro')	
	plt.show()


