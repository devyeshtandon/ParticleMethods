from simulation import simulationInit
from Plotting import plotBoxes, plotQuiver2
from node import NodeMain
import matplotlib.pyplot as plt

particles = simulationInit()
nodes, tree = NodeMain(particles)

plt.axes()
plt = plotBoxes(nodes, plt)

plt = plotQuiver2(particles, plt)
plt.axis('scaled')
plt.show()



