from numpy import savetxt
from numpy import zeros

def SaveData(Elements, t):
	X = zeros(len(Elements))*1.0j
	C = [""]*len(Elements)
	for i in range(len(Elements)):
		X[i] = Elements[i].xy
		if Elements[i].strength >0:
			C[i] = "r"
		else:
			C[i] = "b"

	nm = str(str(100*t)+'.txt')
	cm = str(str(100*t)+'c.txt')

	savetxt(nm, X.view(float).reshape(-1, 2))
	savetxt(cm, C, delimiter=" ,", fmt="%s")
