import numpy as np
from ple.games.flappybird import FlappyBird
from ple import PLE
import pygame as py
import random
import tensorflow
import tensorflow.keras.layers as Kl
import tensorflow.keras.models as Km
import tensorflow.keras as keras
# from PIL import Image
import time

filename = "/Users/admin/Desktop/FBv/flappy_vfunc5/vfunc_v5_12_model"
model = Km.load_model(filename)

# tensorflow.random.set_seed(24)

def get_state(info,action):
	y = info["next_pipe_top_y"] - info["player_y"] # good if > 0
	x = info["next_pipe_dist_to_player"] # how does this work if the bird is already in the pipe?
	vel = info["player_vel"]
	diff = info["next_next_pipe_dist_to_player"] - info["next_pipe_dist_to_player"]
	# x_y_vel_diff
	state = np.array([[x,y,vel,diff,action]])
	return state

# game setting
game = FlappyBird()

rewards = {"loss":-1000,"tick":0}
p = PLE(game, fps=30, display_screen=True, force_fps=False, reward_values=rewards)
 # fps=30, display_screen=True, force_fps=False
# tick --> every time step (frame) = 0 reward
# positive --> every pass through pipe = 1 reward
# loss --> bird dies by crashing into pipe reward
p.init()
reward = 0.0
# params setting
sessions = 10
rewards = np.zeros(sessions)

for i in range(sessions):
	print("Round {}".format(i))
	# in state, first int is to rep if its prev or next state, second digit rep actions
	state0_0 = get_state(p.getGameState(),0)
	state0_1 = get_state(p.getGameState(),1)
	frame = 0
	while True:
		if reward > 0:
			rewards[i] += reward
		if p.game_over(): #check if the game is over
			p.reset_game()
			break
		# obs = p.getScreenRGB()
		# im = Image.fromarray(obs)
		# im.save("/Users/admin/Desktop/frames/your_file_{}.jpeg".format(str(frame)))
		# dictionary to describe state
		# need to make function to choose action
		# start = time.time()
		# v0_0 = model.predict(state0_0)
		# v0_1 = model.predict(state0_1)
		v0_0 = model(state0_0,training=False)
		v0_1 = model(state0_1,training=False)
		# end = time.time()
		print(v0_0,v0_1)
		action = None if v0_0 > v0_1 else 119
		# act(119) to fly, act(None) otherwise
		reward = p.act(action)
		# print(reward)
		state0_0 = get_state(p.getGameState(),0)
		state0_1 = get_state(p.getGameState(),1)
		frame += 1

print(rewards)

