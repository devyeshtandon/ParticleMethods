from ps import initialize, propogate
from numpy import arange, zeros
import matplotlib.pyplot as plt

def setup():
	[Pa, h] = initialize();
	dt = 0.001
	time = arange(0, 0.1, dt)

	for t in range(len(time)):
		print t
		[Pa, h] = propogate(Pa, h, dt)
	plotGraph(Pa)

def plotGraph(Pa):
        x = zeros(len(Pa))
        y = zeros(len(Pa))
        for i in range(len(Pa)):
                y[i] = Pa[i].rho
                x[i] = Pa[i].x

        plt.plot(x, y)
        plt.show()


if __name__ == '__main__':
	setup();
