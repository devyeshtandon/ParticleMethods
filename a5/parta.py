from simulation1 import simulationInit
from Plotting import plotBoxes
from node import NodeMain
import matplotlib.pyplot as plt

particles = simulationInit()

nodes, tree = NodeMain(particles)

plt.axes()

plt = plotBoxes(nodes, plt)

plt.axis('scaled')
plt.show()



