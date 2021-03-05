import pickle
import matplotlib.pyplot as plt
import numpy as np

fr = open('/Users/admin/Desktop/FYP/tictactoe/tabular/state_converge_O', 'rb')
states_converge = pickle.load(fr)
fr.close()

for i in range(1,10):
	plt.plot(np.linspace(0,20,len(states_converge[i])),states_converge[i])

plt.ylim((0,0.4))
plt.xlabel("Episodes/1000 games",fontsize=12)
plt.ylabel("State values of opening position",fontsize=12)
# plt.xticks(np.arange(0,21),np.arange(0,21))
plt.xticks(np.arange(0,21,2),np.arange(0,21,2),fontsize=12)
plt.yticks([0.0,0.1,0.2,0.3,0.4],[0.0,0.1,0.2,0.3,0.4],fontsize=12)
plt.legend(["1","2","3","4","5","6","7","8","9"],fontsize=11)
plt.savefig('/Users/admin/Desktop/tictactoe.png')

