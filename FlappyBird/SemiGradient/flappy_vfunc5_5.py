import numpy as np
from ple.games.flappybird import FlappyBird
from ple import PLE
import pygame as py
import random
import tensorflow
import tensorflow.keras.layers as Kl
import tensorflow.keras.models as Km
import tensorflow.keras as keras
import os
import pickle

filename = "/home/svu/e0235225/FYP/Flappy_bird/vfunc_v5_10_model"
model_trained = Km.load_model(filename)

tensorflow.random.set_seed(106)

def get_state(info,action):
	y = info["next_pipe_top_y"] - info["player_y"] # good if > 0
	x = info["next_pipe_dist_to_player"] # how does this work if the bird is already in the pipe?
	vel = info["player_vel"]
	diff = info["next_next_pipe_dist_to_player"] - info["next_pipe_dist_to_player"]
	# x_y_vel_diff
	state = np.array([[x,y,vel,diff,action]])
	return state

def format_state(state):
	state1 = str(state[0,0])+"_"+str(state[0,1])+"_"+str(state[0,2])+"_"+str(state[0,3])
	action1 = 0 if state[0,4] else 1
	return state1, action1

try:
    os.environ["DISPLAY"]
except:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

# game setting
game = FlappyBird()

rewards = {"loss":-10,"tick":0.5}
p = PLE(game, reward_values=rewards)
 # fps=30, display_screen=True, force_fps=False
# tick --> every time step (frame) = 0 reward
# positive --> every pass through pipe = 1 reward
# loss --> bird dies by crashing into pipe reward
p.init()

# params setting
reward = 0.0
sessions = 20000
lr = 0.0001
gamma = 0.9
exp = 0.8
exp_factor = 0.997
t = 0

# model setting
model = Km.Sequential()
model.add(Kl.Dense(8, activation='relu' ,input_dim=5))
model.add(Kl.Dense(8, activation='relu'))
model.add(Kl.Dense(1, activation='linear'))
# optimzer is how do you want to minimise your loss function and admams is gradient descent with varying step size 
opt = keras.optimizers.SGD(learning_rate=lr,clipnorm=1.0)
model.compile(optimizer=opt, loss='mean_squared_error', metrics=['accuracy'])
model.summary()

filename = "/home/svu/e0235225/FYP/Flappy_bird/q_val_v3"
infile = open(filename,'rb')
q_val = pickle.load(infile)
weights = np.array(model_trained.get_weights(),dtype='object')
model.set_weights(weights)

for i in range(sessions):
	if i%1000==0:
		print("Round {}".format(i))
		exp *= exp_factor
	# in state, first int is to rep if its prev or next state, second digit rep actions
	state0_0 = get_state(p.getGameState(),0)
	state0_1 = get_state(p.getGameState(),1)
	while True:
		if p.game_over(): #check if the game is over
			t = 0
			p.reset_game()
			break
		# obs = p.getScreenRGB()
		# dictionary to describe state
		# need to make function to choose action
		if t == 0:
			v0_0 = model(state0_0,training=False)
			v0_1 = model(state0_1,training=False)
			t = 1
		if np.random.uniform(0, 1) <= exp:
			action = np.random.choice([119,None])
		else:
			if v0_0 == v0_1:
				action = np.random.choice([119,None])
			elif v0_0 > v0_1:
				action = None
			else: action = 119
		state0 = state0_1 if action else state0_0
		# act(119) to fly, act(None) otherwise
		reward = p.act(action)
		state1_0 = get_state(p.getGameState(),0)
		state1_1 = get_state(p.getGameState(),1)
		if format_state(state0) in q_val.keys():
			# print("here!")
			vals, indx = q_val[format_state(state0)]
			target = vals[indx]
			model.fit(state0, np.array([target]), epochs=10, verbose=0)
		else:
			v1_0 = model(state1_0,training=False)
			v1_1 = model(state1_1,training=False)
			# this is the update	
			v_s_tag = max(v1_0,v1_1)
			target = np.array(reward + gamma*v_s_tag)
			model.fit(state0, target, epochs=10, verbose=0)
		state0_0 = state1_0
		state0_1 = state1_1
		v0_0 = v1_0 
		v0_1 = v1_1


print("done")
model.save("/home/svu/e0235225/FYP/Flappy_bird/vfunc_v5_12_model")









