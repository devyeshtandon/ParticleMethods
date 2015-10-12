from numpy import pi, sqrt, exp

def Gaussian1D(h, q):
	temp = 1.0/sqrt(pi)/h*exp(-q**2)
	return temp

def CubicSpline1D(h, q):
	q = abs(q)
	if q<1.0:
		temp = 2.0/3/h*(1.0-(3.0/2.0*(q**2)*(1.0-q/2)))
	elif q<2.0:
		temp = 2.0/12/h*(2-q)**3
	else:
		temp = 0

	return temp	

def DerCubicSpline1D(h, q):
	if q>0:
		sign = 1
	else:
		sign = -1

	q = abs(q)
        if q<1.0:
                temp = (-2.0*q/h + 1.5*q**2/h)/h
        elif q<2.0:
                temp = -1.0/2.0/(h**2)*(2-q)**2
        else:
                temp = 0

        return temp*sign 

def DerGaussian1D(h,q):
	if q>0:
		sign = 1
	else:
		sign = -1

	q = abs(q)
	temp = -2.0*q/(h**2)/sqrt(pi)*exp(-q**2)
	return temp*sign
