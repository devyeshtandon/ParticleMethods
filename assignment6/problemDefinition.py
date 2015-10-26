from numpy import arange, zeros, concatenate, ones
from kernalDefinitions import CubicSpline1D, DerCubicSpline1D
import matplotlib.pyplot as plt

def initialize():
	xl = arange(-0.5, 0, 0.0015625)
	xr = arange(0 ,0.50625, 0.00625)
	x = concatenate((xl, xr), 1)
	p = zeros(len(x))
	rho = zeros(len(x))
	u = zeros(len(x))
	m = zeros(len(x))
	for i in range(len(x)):
		if x[i]<0:
			p[i] = 1.0
			u[i] = 0.0
			rho[i] = 1.0
			m[i] = 0.0015625
		else:
			p[i] = 0.1
			u[i] = 0.0
			rho[i] = 0.25
			m[i] = 0.0015625

	h  = 2*0.00625

	return [x, p, rho, u, m, h]

def propogate(x, p, rho, u, m, h, dt):
	rho = propogaterho(rho, m, x, h);
	dv  = propogatev(u, p, x, rho, h, m)
#	xsph = xphterm(rho, m, u)	

#	x = x + u*dt + xsph
#	u = u + dv*dt;
	return  [x, p , rho, u]
	
def ghosting(var):
        ghost = ones(len(var))
        newvar = concatenate((ghost*var[0], var), 1)
        newvar = concatenate((newvar, ghost*var[len(var)-1]), 1)
	return newvar

def xghost(x):
        xl = arange(-1.5-0.0015625,-0.5, 0.0015625);
        xr = arange(0.5,1.50625, 0.00625);
        xn = concatenate((xl, x), 1);
        xn = concatenate((xn, xr), 1);
	return xn

def propogatev(u, p, x, rho, h, m):
	newrho = ghosting(rho)
	newu = ghosting(u)
	newp = ghosting(p)
	newm = ghosting(m)
	xn = xghost(x)

	dvVal = zeros(len(rho))

	for i in range(len(u)):
		summ = 0
		for j in range(len(newu)):
			a = len(rho) + 1 + i;
			b = j
			Wab = xn[a] - xn[b]
			temp = DerCubicSpline1D(h, float(Wab))
			if ((newu[a]-newu[b])*Wab)<0:
				piab = calculateViscosity(float(newp[a]), float(newu[a]), float(newrho[a]), float(newp[b]), float(newu[b]), float(newrho[b]));
			else:
				piab = 0
			
			summ += newm[b]*(newp[a]/(newrho[a]**2) + newp[b]/(newrho[b]**2) + piab)*temp	

		dvVal[i] = -summ
	plt.plot(x, dvVal)
	plt.show()
	return dvVal

def propogaterho(rho, m, x, h):

	newrho = ghosting(rho)
	newm = ghosting(m)
        rhoVal = zeros(len(rho))

	xn = xghost(x)
        for i in range(len(rho)):
                summ = 0
                for j in range(len(newrho)):
                        Wab = xn[len(rho)+1+i] - xn[j]
                        temp = CubicSpline1D(h, float(Wab))
                        summ += newm[j]*newrho[j]*temp
                rhoVal[i] = summ

        return rhoVal
	


