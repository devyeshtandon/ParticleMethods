from numpy import loadtxt, arange, genfromtxt
import pylab

pylab.ion()

nm = []
cm = []
sv = []
for t in arange(0, 3, 0.1):
	nm.append(str(str(100*t)+'.txt'))
	cm.append(str(str(100*t)+'c.txt'))
	sv.append(str('pics/'+str(100*t)+'.png'))


counter = 0
for i in nm:
	array = loadtxt(i).view(complex).reshape(-1)
	C = genfromtxt(cm[counter], delimiter=" ,", dtype=None)
	
	X = [j.real for j in array]
	Y = [j.imag for j in array]

	pylab.scatter(X, Y, c=C, s=7)
	pylab.axis([-2, 2, 2, -2])
	pylab.gca().set_aspect('equal', adjustable='box')
	pylab.draw()
	pylab.savefig(sv[counter])

	counter += 1
	pylab.clf()
raw_input()

 
