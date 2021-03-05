import numpy as np
import tensorflow
import tensorflow.keras.layers as Kl
import tensorflow.keras.models as Km
import tensorflow.keras as keras
import pickle
import copy
from .player import Player

BOARD_ROWS = 3
BOARD_COLS = 3

tensorflow.random.set_seed(535)

class VfuncBot():
	def __init__(self, player, exp_rate=0.8):
		self.player = player
		self.lr = 0.1
		self.model = self.create_model()
		self.exp_rate = exp_rate

	def create_model(self):
		model = Km.Sequential()
		model.add(keras.Input(shape=(2,9)))
		model.add(Kl.Dense(128, activation='relu'))
		model.add(Kl.Flatten())
		model.add(Kl.Dense(128, activation='relu'))
		model.add(Kl.Dense(1, activation='linear'))
		# optimzer is how do you want to minimise your loss function and admams is gradient descent with varying step size 
		opt = keras.optimizers.SGD(learning_rate=0.001)
		model.compile(optimizer=opt, loss='mean_squared_error', metrics=['accuracy'])
		model.summary()
		return model

	def format_board(self, board):
		state = np.zeros((1,2,9))
		for i in range(0,len(board)):
			for j in range(0,len(board)):
				if board[i][j]==Player.x:
					state[0,0,i*3+j] = 1
					state[0,1,i*3+j] = 0
				elif board[i][j]==Player.o:
					state[0,1,i*3+j] = 1
					state[0,0,i*3+j] = 0
				else: 
					state[0,0,i*3+j] = 0
					state[0,1,i*3+j] = 0
		return state

	def select_move(self, board):
		positions = board.get_legal_moves()
		# possible actions
		PA = []
		if np.random.uniform(0, 1) <= self.exp_rate:
			# take random action
			idx = np.random.choice(len(positions))
			action = positions[idx]
		else:
			value_max = -999
			for p in positions:
				newboard = copy.deepcopy(board)
				# print(newboard.grid,p)
				newboard.make_move(p[0], p[1], self.player)
				# print(newboard.grid)
				# create format_board function
				value = self.calc_value(newboard.grid)
				# print(value)
				# print("value", value)
				if value > value_max:
					value_max = value
					PA = []
					PA.append(p)
				elif value == value_max:
					PA.append(p)
			if len(PA) == 0:
				print("no actions in possible actions list...")
			elif len(PA) == 1:
				action = PA[0]
			else:
				action = PA[np.random.choice(len(PA))]
			# print("{} takes action {}".format(self.name, action))
		return action

	def calc_value(self, state):
		state = self.format_board(state)
		# print(state)
		return self.model.predict(state)

	def calc_target(self,state,prev_state,reward):
		v_s = self.calc_value(prev_state)
		if reward == 0:
			v_s_tag = self.calc_value(state)
		else:
			v_s_tag = np.array([[0]])
		target = np.array(self.lr * (reward + v_s_tag))
		return target

	# at the end of game, backpropagate and update states value based on the previous state
	def feedReward(self,state,prev_state,reward):
		target = self.calc_target(state,prev_state,reward)
		prev_state = self.format_board(prev_state)
		self.model.fit(prev_state, target, epochs=10, verbose=0)

	def savePolicy(self,file="/home/svu/e0235225/FYP/TicTacToe/Epo_Vmodel1_v11"):
		self.model.save(file)

	def loadPolicy(self, file):
		self.model = Km.load_model(file)

	def check(self,board):
		# board here is a new board.grid
		board1 = copy.deepcopy(board)
		state_p1 = []
		actions = {'1':[0,0],'2':[0,1],'3':[0,2],'4':[1,0],'5':[1,1],'6':[1,2],'7':[2,0],'8':[2,1],'9':[2,2]}
		for i in range(1,10):
			board1[actions[str(i)][0]][actions[str(i)][1]] = self.player
			x = self.calc_value(board1)
			state_p1.append(x)
			board1[actions[str(i)][0]][actions[str(i)][1]] = None
		return state_p1
