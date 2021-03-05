import numpy as np
import pickle
import matplotlib.pyplot as plt
from statistics import *

fr1 = open('/Users/admin/Desktop/RandomML-master/v6/wins_EpoV1_v6', 'rb')
wins7 = pickle.load(fr1)
fr1.close()

fr2 = open('/Users/admin/Desktop/RandomML-master/v12/states_EpoV1_v12', 'rb')
states = pickle.load(fr2)
labels = []
fr2.close()

for i in range(0,9):
	# policy
	# plt.plot(np.linspace(0,len(states),len(states)),list(map(lambda x: x[0][i],states)))
	# # value
	plt.plot(np.arange(0,len(states)),list(map(lambda x: x[i][0][0],states)))
	labels.append(i+1)

# plt.vlines([5,10],-0.05,0.05,linestyles='dashed')
plt.legend(labels,loc='upper right')
plt.xlabel("training/1000 games")
plt.ylabel("state values")
plt.xticks(np.arange(0,len(states)),np.arange(0,len(states)))
# plt.ylim([-0.05,0.05])
plt.savefig('/Users/admin/Desktop/states2.png')


#########################################################################################

for i in range(0,3):
	plt.plot(np.arange(0,len(wins7[i])),wins7[i],'-o',linewidth=0.3)
# plt.axhline(mean(wins7[1]),linestyle='dashed',color='black')

plt.ylim([0,100])
plt.xlabel("training/1000 games",fontsize=12)
plt.xticks(np.arange(0,len(wins7[i])),np.arange(0,len(wins7[i])),fontsize=12)
# print(mean(wins7[1]))
plt.legend(['lose','draw','win'],fontsize=11)

plt.title('Reward 1 for a draw')
plt.ylabel(r"games won against $\epsilon$-minimax player",fontsize=12)
plt.yticks(fontsize=12)
plt.savefig('/Users/admin/Desktop/p1wins_03.png')

plt.figure(2)
for i in range(0,3):
	plt.plot(np.arange(0,len(wins4[i])),wins4[i],'-o',linewidth=0.3)
# plt.axhline(mean(wins4[1]),linestyle='dashed',color='black')

# print(mean(wins4[1]))
# plt.vlines([5,10],0,100,linestyles='dashed')
plt.ylim([-5,105])
plt.xlabel("training/1000 games",fontsize=12)
plt.xticks(np.arange(0,len(wins4[i])),np.arange(0,len(wins4[i])),fontsize=12)
plt.legend(['lose','draw','win'],fontsize=11)
plt.title('Reward 0.1 for a draw')
plt.ylabel("games won against minimax player",fontsize=12)
plt.yticks(fontsize=12)
plt.savefig('/Users/admin/Desktop/p1winsPv2.png')
