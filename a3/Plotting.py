import pylab

def plotInit():
	pylab.ion()
	graph, = pylab.plot(1, 'ro', markersize = 6) 
	x = 6
	pylab.axis([-x,x,x,-x])

	graph.set_xdata(0)
	graph.set_ydata(0)
	pylab.draw()
	return graph

def plotData(X, Y, Graph):
	Graph.set_xdata(X)
	Graph.set_ydata(Y)
	pylab.draw()

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
	plotData(X, Y, Graph)	
	panelPlot(Panels)

def plotParticles(Elements, Panels, Graph):

	X = [i.xy.real for i in Elements]
	Y = [i.xy.imag for i in Elements]
	plotData(X, Y, Graph)
	panelPlot(Panels)
