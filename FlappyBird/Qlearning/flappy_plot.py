import numpy as np
import pickle
import matplotlib.pyplot as plt

filename = "/Users/admin/Desktop/points_v"

infile = open(filename,'rb')
points = pickle.load(infile)
infile.close()

print(points)

y = list(map(lambda x: -x[2],points))[:130]
action = list(map(lambda x: x[3],points))[:130]
indx = []
plt_act = []
w = 8

for i,j in enumerate(action):
	if j:
		indx.append(i)

for i in indx:
	plt_act.append(y[i])

plt.plot(np.arange(0,len(y)),y)
plt.plot(indx,plt_act,'rx')
plt.plot([78,78],[-244,-300],color='green')
plt.plot([78,78],[0,-144],color='green')
plt.plot([114,114],[-260,-300],color='green')
plt.plot([114,114],[-0,-160],color='green')
plt.plot([78-w,78-w],[-244,-300],color='green')
plt.plot([78-w,78-w],[0,-144],color='green')
plt.plot([114-w,114-w],[-260,-300],color='green')
plt.plot([114-w,114-w],[-0,-160],color='green')
plt.legend(['flight path','flap','pipe'],fontsize=11)
plt.ylabel("position",fontsize=12)
plt.xlabel("time step",fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig('/Users/admin/Desktop/flappy_visualV.png')