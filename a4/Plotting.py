import pylab
from numpy import shape
from numpy import zeros, sqrt

def plotInit(Plotting, Elements):
	if (Plotting == 2):
		loc = [i.xy for i in Elements]
		x = [i.real for i in loc]
		y = [i.imag for i in loc]
		x = list(sorted(set(x))) 
		x.remove(-10)
		y = list(sorted(set(y)))

		X, Y = pylab.meshgrid(x, y)
		U = pylab.ones(shape(X))
		V = pylab.ones(shape(Y))

		pylab.ion()
		fig, ax = pylab.subplots(1,1)
		graph = ax.quiver(X, Y, U, V)
		pylab.draw()
	else:
		pylab.ion()
		graph, = pylab.plot(1, 'ro', markersize = 2) 
		x = 2
		pylab.axis([-x,x,x,-x])

		graph.set_xdata(0)
		graph.set_ydata(0)
		pylab.draw()

	return graph

def plotData(X, Y, C, t):

	pylab.clf()
	x = 2 
        pylab.axis([-x,x,x,-x])
	pylab.scatter(X, Y, c=C, s=7)

	pylab.draw()
	pylab.savefig(str(100*t)+".png")

def panelPlot(Panels):
	points = [i.z1 for i in Panels]
	X = [i.real for i in points]
	X.append(points[0].real)
	Y = [i.imag for i in points]
	Y.append(points[0].imag)
	pylab.plot(X,Y)

def plotPathLine(Elements, Panels, Graph, X, Y):
	X.extend(i.xy.real for i in Elements)
	Y.extend(i.xy.imag for i in Elements)
	C = gammaColor(Elements)
	plotData(X, Y, C)	
	panelPlot(Panels)

def plotParticles(Elements, Panels, Graph, t):

	X = [i.xy.real for i in Elements]
	Y = [i.xy.imag for i in Elements]
	C = gammaColor(Elements)
	plotData(X, Y, C, t)
	panelPlot(Panels)

def gammaColor(Elements):
	color = [""]*len(Elements)
	for i in range(len(Elements)):
		try:
			if (Elements[i].strength < 0):
				color[i] = "r"
			else:
				color[i] = "b"
		except:
			color[i] = "r"
	return color

def plotQuiver(fieldValue1, fieldValue2, graph, dim, allElements, Panels):
	panelPlot(Panels)
	vel = zeros(dim)*1j

	for i in range(dim):
		for j in range(allElements):
			vel[i] += (fieldValue1[j][i] + fieldValue2[j][i])/2

	u = [i.real for i in vel]
	v = [i.imag for i in vel]

	dim =20
	U = zeros([dim, dim])
	V = zeros([dim, dim])

	for i in range(dim):
		for j in range(dim):
			U[i][j] = u[j*dim + i]
			V[i][j] = v[j*dim + i]

	graph.set_UVC(U, V)
	pylab.draw()

def PlotAll(Elements, Panels, FieldRK2, FieldEuler, Graph, X, Y, t, plottingType):
        if plottingType == 1:
                plotPathLine(Elements, Panels, Graph, X, Y)
        elif plottingType == 0:
                plotParticles(Elements, Panels, Graph, t)
        elif plottingtype == 2:
                plotQuiver(FieldRK2, FieldEuler, Graph, numOfQE, NumOfElements, Panels)
	
