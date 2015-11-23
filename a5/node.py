from numpy import zeros, real, imag, conj

class Node(object):
	particleIndex = 0
	strength = 0
	center = 0 + 0j
	vertex = 1 - 1j

	def __init__(self, c, v):
		self.center = c
		self.vertex = v

def isInside(x, c, v):
	'''
	print x, v, c
	print real(x)
	print real(v)
	print real(2*c-v)

	print imag(x)
	print imag(v)
	print imag(2*c-v)
	raw_input()
	'''
	if(real(x)<=real(v)) & (real(x)>real(2*c-v)):
		if(imag(x)>=imag(v)) & (imag(x)<imag(2*c-v)):
			return True
	return False

def noOfParticlesInside(particles, N):
	n = 0
	c = N.center
	v = N.vertex
	indx = []
	for i in range(len(particles)):
		if isInside(particles[i].xy, c, v):
			n = n+1
			indx.append(i)

	return n, indx


def childGeneration(N, particles, tree, i):
	maxInCell = 10
	p, t = (noOfParticlesInside(particles, N[i]))
	
	N[i].particleIndex = t
	if (p > maxInCell):
		t = len(N)
		tree[i] = [t, t+1, t+2, t+3]
		c = N[i].center
		v = N[i].vertex 
		N.append(Node((c-(v-c)/2), c))
		N.append(Node((c+(v-c)/2), v))
		N.append(Node(c+(conj(v-c)/2), real(v) + 1j*imag(c)))
		N.append(Node(c-(conj(v-c)/2), real(c) + 1j*imag(v)))
		tree.append([])
		tree.append([])
		tree.append([])
		tree.append([])
		for k in tree[i]:
			childGeneration(N, particles, tree, k)		
	
		
	
def NodeMain(particles):
	N = []
	tree = [[]]
	initC = 0
	initV = 2 - 2j
	N.append(Node(initC, initV))
	childGeneration(N, particles, tree, 0)
	return N, tree

