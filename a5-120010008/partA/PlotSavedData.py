from numpy import loadtxt, arange, genfromtxt, meshgrid, reshape, transpose, asarray, shape
import pylab

pylab.ion()

nm = []
cm = []
sv = []
for t in arange(0, 5, 0.1):
	nm.append(str(str(100*t)+'.txt'))
#	cm.append(str(str(100*t)+'c.txt'))
	sv.append(str('pics/'+str(100*t)+'.png'))


counter = 0
x = arange(-2, 2, 0.2)
y = arange(-2, 2, 0.2)

X, Y = meshgrid(x, y)

for i in nm:
	array = loadtxt(i).view(complex).reshape(-1)
#	C = genfromtxt(cm[counter], delimiter=" ,", dtype=None)
	
	u = [j.real for j in array]
	v = [j.imag for j in array]
	
	U = asarray(u).reshape(shape(X))
	U = U.transpose()
	
	V = asarray(v).reshape(shape(Y))
	V = V.transpose()

	pylab.quiver(X, Y, U, V)
	pylab.axis([-2, 2, -2, 2])
	pylab.gca().set_aspect('equal', adjustable='box')
	pylab.draw()

	pylab.savefig(sv[counter])

	counter += 1
#	raw_input()
	pylab.clf()

 
