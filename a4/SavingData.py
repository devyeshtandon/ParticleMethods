from numpy import savetxt
from numpy import zeros

def SaveData(Elements):
	X = zeros(len(Elements))*1.0j
	for i in range(len(Elements)):
		X[i] = Elements[i].xy

	savetxt('_data.txt', X)
