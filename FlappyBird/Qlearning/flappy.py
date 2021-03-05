import numpy as np
from ple.games.flappybird import FlappyBird
from ple import PLE
import pygame as py
import random
import pickle
import os

filename = "q_val_v2"
infile = open(filename,'rb')
q_val = pickle.load(infile)
# q_val = {}
infile.close()

def get_state(info):
	y = info["next_pipe_top_y"] - info["player_y"] # good if > 0
	x = info["next_pipe_dist_to_player"] # how does this work if the bird is already in the pipe?
	vel = info["player_vel"]
	diff = info["next_next_pipe_dist_to_player"] - info["next_pipe_dist_to_player"]
	# x_y_vel_diff
	state = str(x)+"_"+str(y)+"_"+str(vel)+"_"+str(diff)
	return state

try:
    os.environ["DISPLAY"]
except:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

game = FlappyBird()

rewards = {"loss":-1000,"tick":0.5}
p = PLE(game, reward_values=rewards)
 # fps=30, display_screen=True, force_fps=False
# tick --> every time step (frame) = 0 reward
# positive --> every pass through pipe = 1 reward
# loss --> bird dies by crashing into pipe reward
p.init()

reward = 0.0
sessions = 100000
lr = 0.7
gamma = 1

for i in range(sessions):
	if i%1000==0:
		print("Round {}".format(i))
	state0 = get_state(p.getGameState())
	while True:
		if p.game_over(): #check if the game is over
			p.reset_game()
			break
		obs = p.getScreenRGB()
		# dictionary to describe state
		# need to make function to choose action
		if state0 not in q_val.keys():
			q_val[state0] = [0,0]
			action = random.choice(p.getActionSet())
		else:
			if max(q_val[state0]) == 0:
				action = random.choice(p.getActionSet())
			else:
				if q_val[state0][0] >= q_val[state0][1]:
					action = 119
				else:
					action = None
		# act(119) to fly, act(0) otherwise
		reward = p.act(action)
		state1 = get_state(p.getGameState())
		if state0 not in q_val.keys():
		# qval[state0] is a list, 0 to fly, 1 to not
			q_val[state0] = [0,0]
		if state1 not in q_val.keys():
			q_val[state1] = [0,0]
		action = 0 if action else 1
		# this is the update	
		q_val[state0][action] = (1-lr)*q_val[state0][action] + lr*(reward+gamma*max(q_val[state1]))
		state0 = state1

filename = "q_val_v3"
outfile = open(filename,'wb')
pickle.dump(q_val,outfile)
outfile.close()
