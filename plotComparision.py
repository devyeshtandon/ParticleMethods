import sys
sys.path.append('/home/devyesh/Documents/Sem 7/ParticleMethods/a3b')
sys.path.append('/home/devyesh/Documents/Sem 7/ParticleMethods/a2')
sys.path.append('/home/devyesh/Documents/Sem 7/ParticleMethods/a3cd')

from mainCode import del2
from mainCode1 import delta
from mainCode2 import delta2

from numpy import zeros

err = zeros(shape=(100,1))
err2 = zeros(shape=(100,1))
for i in range(100):
	X = del2(i/100)
#	Y = delta(i/100)
	Z = delta2(i/100)
	E = [X[i]-Y[i] for i in range(len(X))]
	E1 = [X[i]-Z[i] for i in range(len(X))]
	err[i] = max(E1)
	err2[i] = max(E) 
	print X
