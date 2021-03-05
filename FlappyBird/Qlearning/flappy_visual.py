import numpy as np
from ple.games.flappybird import FlappyBird
from ple import PLE
import pygame as py
import random
import pickle
from PIL import Image

filename = "/Users/admin/Desktop/FYP/Flappy_bird/flappy_qlearning/q_val"

infile = open(filename,'rb')
q_val = pickle.load(infile)
infile.close()

def get_state(info):
	y = info["next_pipe_top_y"] - info["player_y"] # good if > 0
	x = info["next_pipe_dist_to_player"] # how does this work if the bird is already in the pipe?
	vel = info["player_vel"]
	diff = info["next_next_pipe_dist_to_player"] - info["next_pipe_dist_to_player"]
	# x_y_vel_diff
	state = str(x)+"_"+str(y)+"_"+str(vel)+"_"+str(diff)
	return state

game = FlappyBird()

rewards = {"loss":-1000,"tick":0.5}
p = PLE(game, fps=30, display_screen=True, force_fps=False, reward_values=rewards)
# tick --> every time step (frame) = 0 reward
# positive --> every pass through pipe = 1 reward
# loss --> bird dies by crashing into pipe reward
p.init()

reward = 0.0
sessions = 1
points = []

for i in range(sessions):
	while True:
		if p.game_over(): 
			p.reset_game()
			break
		state_rep = p.getGameState()
		state0 = get_state(state_rep)
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
		points.append([state_rep["next_pipe_top_y"],state_rep["next_pipe_bottom_y"],state_rep["player_y"],action])
		reward = p.act(action)

fw = open('/Users/admin/Desktop/points_v1','wb')
pickle.dump(points, fw)
fw.close()
