import numpy as np
def exactSol(x,t=0.2,x0=0,ql=[1.,1.,0.],qr=[0.25,0.1,0.],gamma=1.4):
	''' Gives exact solution to Sod shock tube problem in order to check for accuracies and compare with computational solution.
	Exact solution is given at x points.
	Algorith taken from http://www.phys.lsu.edu/~tohline/PHYS7412/sod.html
	Ref. Sod, G. A. 1978, Journal of Computational Physics, 27, 1-31.
	'''
	
	#Import stuff
	from sympy.solvers import nsolve
	from sympy import Symbol
	
	#Initiate stuff
	
	shape=x.shape
	x=x.flatten()
	p1 = Symbol('p1')
	[rol,pl,vl]=ql
	[ror,pr,vr]=qr
	
	#Calculate wave velocities and values
	
	cleft=(gamma*pl/rol)**(0.5)
	cright=(gamma*pr/ror)**(0.5)
	m=((gamma-1)/(gamma+1))**0.5
	eq=((2*(gamma**0.5))/(gamma-1)*(1-(p1**((gamma-1)/2/gamma))))-((p1-pr)*(((1-(m**2))**2)*((ror*(p1+(m*m*pr)))**(-1)))**(0.5))
	ppost=float(nsolve(eq,p1,0.))
	rpostByrright=((ppost/pr)+(m*m))/(1+((ppost/pr)*(m*m)))
	vpost=(2*(gamma**0.5))/(gamma-1)*(1-(ppost**((gamma-1)/2/gamma)))
	romid=((ppost/pl)**(1/gamma))*rol
	vshock=vpost*(rpostByrright)/(rpostByrright-1)
	ropost=rpostByrright*ror
	pmid=ppost
	vmid=vpost

	#Calculate locations
	x1=x0-(cleft*t)
	x3=x0+(vpost*t)
	x4=x0+(vshock*t)
	ro=[]
	p=[]
	v=[]
	for i in x:
		csound=((m*m)*(x0-i)/t)+((1-(m*m))*cleft)
		vinst=(1-(m*m))*(((i-x0)/t)+cleft)
		roinst=rol*((csound/cleft)**(2/(gamma-1)))
		pinst=pl*((roinst/rol)**(gamma))
		if i<x1:
			ro.append(rol)
			p.append(pl)
			v.append(vl)
		elif (i>=x4):
			ro.append(ror)
			p.append(pr)
			v.append(vr)
		elif (i<x4) and (i>=x3):
			ro.append(ropost)
			p.append(ppost)
			v.append(vpost)
		elif (i<x3) and (((roinst>rol) and (roinst<romid)) or ((roinst<rol) and (roinst>romid))):
			ro.append(roinst)
			p.append(pinst)
			v.append(vinst)
		else:
			ro.append(romid)
			p.append(pmid)
			v.append(vmid)
			
	#Reshape solutions
	ro=np.array(ro).reshape(shape)
	v=np.array(v).reshape(shape)
	p=np.array(p).reshape(shape)
	
	#calculate conserved variables
	rou = ro*v
	ener=p/(gamma-1)/ro

	return([ro,v,p,ener])
