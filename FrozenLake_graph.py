import pickle
import numpy as np
import matplotlib.pyplot as plt

fw = open('/Users/admin/Desktop/test_rate', 'rb')
rate = pickle.load(fw)
fw.close()

print(rate)

sessions = 2500

plt.plot(np.arange(1,sessions+1,100),rate)
plt.ylim([0,100])
plt.xlabel('Episodes',fontsize=12)
plt.ylabel('Success in 100 episodes',fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig('/Users/admin/Desktop/train_success_rate.png')
