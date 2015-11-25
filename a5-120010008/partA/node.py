from numpy import zeros, real, imag, conj, linalg
from math import factorial, pi
from elementDefinition import CalculateFieldE

noOfTerms = 15

class Node(object):
	particleIndex = []
	index = 0
	strength = 0
	center = 0 + 0j
	vertex = 1 - 1j
	aj = 0

	def __init__(self, c, v, idx):
		self.center = c
		self.vertex = v
		self.index = idx

	def radius(self):
		return abs(self.center-self.vertex)
	
	def directVelocity(self, p, part):
		v = 0
		for i in self.particleIndex:	
			v += part[i].fieldValue(p.xy)
		return v	

	def multipoleEx(self, p):
		v = 0
		for i in range(noOfTerms):
			v += -1.0j/2.0/pi*self.aj[i]/(pow((p.xy-self.center), i+1))
		return conj(v)

def isInside(x, c, v):
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

def combitorial(a, b):
	return factorial(a)/factorial(b)/factorial(a-b)

def childGeneration(N, particles, tree, i):
	maxInCell = 3
	p, t = (noOfParticlesInside(particles, N[i]))
	N[i].particleIndex = t
	if (p > maxInCell):
		t = len(N)
		tree[i] = [t, t+1, t+2, t+3]
		c = N[i].center
		v = N[i].vertex 
		N.append(Node((c-(v-c)/2), c, t))
		N.append(Node((c+(v-c)/2), v, t+1))
		N.append(Node(c+(conj(v-c)/2), real(v) + 1j*imag(c), t+2))
		N.append(Node(c-(conj(v-c)/2), real(c) + 1j*imag(v), t+3))
		tree.append([])
		tree.append([])
		tree.append([])
		tree.append([])
		for ch in tree[i]:
			childGeneration(N, particles, tree, ch)

		N[i].aj = zeros(noOfTerms)*1j
		for j in range(1, noOfTerms+1):
			for k in range(1, j+1):
				for chi in tree[i]:
					N[i].aj[j-1] += N[chi].aj[k-1]*combitorial(j-1, k-1)*pow((-N[i].center + N[chi].center), j-k)

	else:
		N[i].aj = zeros(noOfTerms)*1j
		for j in range(1, noOfTerms+1):
			for tempIdx in t:
				N[i].aj[j-1] += particles[tempIdx].strength*pow((particles[tempIdx].xy- N[i].center),(j-1))
		

def ComputeCellVelocity(N, i, p, part, tree):
	v = 0
	c = N[i]
	if (abs(c.center-p.xy)>2*c.radius()):
		v = c.multipoleEx(p)

	elif len(tree[i])>0:
		for child in tree[i]:
			v += ComputeCellVelocity(N, child, p, part, tree)

	else:
		v = c.directVelocity(p, part)

	return v

def CalculateVelocity(particles, Nodes, tree):
	# Calculate the lowest level of cell index	
	child = []
	for n in range(len(Nodes)):
		if  len(tree[n]) == 0:
			child.append(n)

	# Calculate velocity for particles in each child cell
	for n in child:
		for pI in Nodes[n].particleIndex:
			particles[pI].velocity = ComputeCellVelocity(Nodes, 0, particles[pI], particles, tree)
	
def NodeMain(particles):
	N = []
	tree = [[]]
	initC = 0
	initV = 2 - 2j
	N.append(Node(initC, initV, 0))
	childGeneration(N, particles, tree, 0)

	CalculateVelocity(particles, N, tree)
	temp = zeros(len(particles))*1j
	for i in range(len(particles)):
		temp[i] = particles[i].velocity
		particles[i].velocity = 0
	CalculateFieldE(particles, 0)
	error = zeros(len(particles))*1j
	for i in range(len(particles)):
		error[i] = temp[i] - particles[i].velocity

	print linalg.norm(error)
	return N, tree
