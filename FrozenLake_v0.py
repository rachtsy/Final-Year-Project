import gym
import random
import pickle
import numpy as np
import matplotlib.pyplot as plt

# dict in dict so its neater to check the values i feel, should be tuple?

# training error doesn't work because take random steps 30% of the time..?
# so did test every 100 rounds 
# but didnt know why always stuck at local maxima...?

def update_state(pre_obs,cur_obs,action,reward,alpha):
	if state_action.get(pre_obs) is None:
		state_action[pre_obs] = {}
		state_action[pre_obs][action] = 0
	if state_action[pre_obs].get(action) is None:
		state_action[pre_obs][action] = 0
	max_val = 0 if state_action.get(cur_obs) is None else max(state_action[cur_obs].values())
	state_action[pre_obs][action] = (1-alpha)*state_action[pre_obs][action]+alpha*(reward+gamma*max_val)

def choose_action(cur_obs):
	if (state_action.get(cur_obs) is None) or (max(state_action[cur_obs].values())==0):
		return env.action_space.sample()
	return max(state_action[cur_obs], key=state_action[cur_obs].get)

def train(sessions):
	print("training\nRound 0...")
	alpha = 0.33
	epsilon = 1
	rate = []
	for i_episode in range(sessions):
		cur_obs = env.reset()
		for t in range(100):
			# env.render()
			if random.uniform(0,1) <= epsilon or not state_action:
				action = env.action_space.sample()
			else:
				action = choose_action(cur_obs)
			pre_obs = cur_obs
			cur_obs, reward, done, info = env.step(action)
			update_state(pre_obs,cur_obs,action,reward,alpha)
			if alpha > 0.001:
				alpha *= 0.9999
			if done:
				if reward and epsilon > 0.001:
					epsilon *= 0.97
				break
		if ((i_episode+1)%100)==0:
			print("Round {}".format(i_episode+1))
			success = test(100)
			rate.append(success)
	env.close()

	fw = open('/Users/admin/Desktop/test_rate', 'wb')
	pickle.dump(rate, fw)
	fw.close()

	return state_action

def test(sessions):
	success = 0
	for i_episode in range(sessions):
		obs = env.reset()
		for t in range(100):
			# env.render()
			action = choose_action(obs)
			obs, reward, done, info = env.step(action)
			if done:
				success += reward
				print("Episode finished after {} timesteps".format(t+1))
				break
	env.close()
	return success

def savePolicy(state_action):
	fw = open('/Users/admin/Desktop/state_action', 'wb')
	pickle.dump(state_action, fw)
	fw.close()

def loadPolicy(file):
	fr = open(file, 'rb')
	states_action = pickle.load(fr)
	fr.close()
	return states_action

if __name__ == "__main__":
	env = gym.make('FrozenLake-v0')
	# print(env.action_space)
	# print(env.observation_space)
	# print(state_action)
	gamma = 0.9
	state_action = {}
	state_action = train(2500)
	# savePolicy(state_action)
	# state_action = loadPolicy('/Users/admin/Desktop/FYP/Frozenlake/state_action')
	# error = test(1)
	# print(error)
	# error_all = []
	# for i in range(1,11):
	# 	error = test(100)
	# 	error_all.append(error)
	# print(error_all)