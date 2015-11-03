from numpy import random, sort, zeros
from ps import binning, fetchBin
import matplotlib.pyplot as plt


class ZP():
	x = 0;

temp = [ZP() for i in range(20)];

rand = random.random(20);
rand = sort(rand)
lol = zeros(20);
print rand
for i in range(20):
	temp[i].x = rand[i]

w = 0.05
#print temp.x
bins = binning(temp, w)
for i in range(20):
	if bins[i] == 0:
		c = 'green'
	if bins[i] == 1:
		c = 'red'
	if bins[i] == 2:
		c = 'blue'
	if bins[i] == 3:
		c = 'yellow'
	if bins[i] == 4:
		c = 'orange'
	if bins[i] == 5:
		c = 'black'
	if bins[i] == 6:
		c = 'pink'
	if bins[i] == 7:
		c = 'skin'
	if bins[i] == 8:
		c = 'violet'
	if bins[i] == 9:
		c = 'magenta'

	plt.scatter(temp[i].x, 0, color=c);

plt.show()

