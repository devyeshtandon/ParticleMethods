from ps import initialize, propogate
from numpy import arange, zeros
import matplotlib.pyplot as plt
from realSol import exactSol

def setup():
	[Pa, h] = initialize();
	dt = 0.001
	time = arange(0, 0.2, dt)

	for t in range(len(time)):
		print t
		[Pa, h] = propogate(Pa, h, dt)
		
	analyticalSolution = exactSol(arange(-0.5,0.5,0.0025))
	plotGraph(Pa, analyticalSolution)

def plotGraph(Pa, AS):
        x = zeros(400)
        y = zeros(400)
        w = zeros(400)
        z = zeros(400)
        a = zeros(400)

        xa = zeros(400)
        ya = zeros(400)
        wa = zeros(400)
        za = zeros(400)
        aa = zeros(400)


        for i in range(400, 800):
                y[i-400] = Pa[i].p
		w[i-400] = Pa[i].rho
		z[i-400] = Pa[i].u
		a[i-400] = Pa[i].e
                x[i-400] = Pa[i].x
	
	xa = arange(-0.5,0.5, 0.0025)
	ya = AS[2]
	wa = AS[0]
	za = AS[1]
	aa = AS[3]


	f, ax = plt.subplots(2, 2)
	ax[0,0].plot(x,a)
	ax[0,0].plot(xa,aa)
	ax[0,0].set_title('Energy Profile')

	ax[0,1].plot(x,w)
	ax[0,1].plot(xa, wa)
	ax[0,1].set_title('Density Profile')

	ax[1,0].plot(x,y)
	ax[1,0].plot(xa, ya)
	ax[1,0].set_title('Pressure Profile')

	ax[1,1].plot(x,z)
	ax[1,1].plot(xa, za)
	ax[1,1].set_title('Velocity Profile')

        plt.show()


if __name__ == '__main__':
	setup();
