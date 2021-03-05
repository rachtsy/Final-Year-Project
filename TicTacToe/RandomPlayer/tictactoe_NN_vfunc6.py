import numpy as np
import tensorflow
import tensorflow.keras.layers as Kl
import tensorflow.keras.models as Km
import pickle

BOARD_ROWS = 3
BOARD_COLS = 3

tensorflow.random.set_seed(2643)

class State:
	def __init__(self, p1, p2):
		self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
		self.p1 = p1
		self.p2 = p2
		self.isEnd = False
		# init p1 plays first
		self.playerSymbol = 1

	def winner(self):
		# row
		for i in range(BOARD_ROWS):
			if sum(self.board[i, :]) == 3:
				self.isEnd = True
				return 1
			if sum(self.board[i, :]) == -3:
				self.isEnd = True
				return -1
		# col
		for i in range(BOARD_COLS):
			if sum(self.board[:, i]) == 3:
				self.isEnd = True
				return 1
			if sum(self.board[:, i]) == -3:
				self.isEnd = True
				return -1
		# diagonal
		diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
		diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
		diag_sum = max(abs(diag_sum1), abs(diag_sum2))
		if diag_sum == 3:
			self.isEnd = True
			if diag_sum1 == 3 or diag_sum2 == 3:
				return 1
			else:
				return -1

		# tie
		# no available positions
		if len(self.availablePositions()) == 0:
			self.isEnd = True
			return 0
		# not end
		self.isEnd = False
		return None

	def availablePositions(self):
		positions = []
		for i in range(BOARD_ROWS):
			for j in range(BOARD_COLS):
				if self.board[i, j] == 0:
					positions.append((i, j))  # need to be tuple
		return positions

	def updateState(self, position):
		self.board[position] = self.playerSymbol
		# switch to another player
		self.playerSymbol = -1 if self.playerSymbol == 1 else 1

	# only when game ends
	def giveReward(self,prev_state,is_Random):
		result = self.winner()
		# backpropagate reward
		if result == 1:
			self.p1.feedReward(self.board,prev_state,1)
			if not is_Random:
				self.p2.feedReward(self.board,prev_state,-1)
		elif result == -1:
			self.p1.feedReward(self.board,prev_state,-1)
			if not is_Random:
				self.p2.feedReward(self.board,prev_state,1)
		else:
			self.p1.feedReward(self.board,prev_state,0.1)
			if not is_Random:
				self.p2.feedReward(self.board,prev_state,0.1)

	# board reset
	def reset(self):
		self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
		self.isEnd = False
		self.playerSymbol = 1

	def play(self, rounds=100):
		wins = np.zeros([3,int(rounds/1000)])
		state0 = []
		show = False
		for i in range(rounds):
			if i % 1000 == 0:
				show = True
				print("Rounds {}".format(i))
				k = int(i/1000)
				p1_exp_rate = p1.exp_rate
				p1.exp_rate = 0
				for j in range(0,100):
					winner = self.play3()
					wins[winner+1,k]+=1
				state0.append(p1.check())
				if wins[2,k] > 70:
					p1.exp_rate = p1_exp_rate*0.99
				elif wins[2,k] > 90:
					p1.exp_rate = 0
				else:
					p1.exp_rate = p1_exp_rate
			while not self.isEnd:
				# Player 1
				if show:
					self.showBoard()
				positions = self.availablePositions()
				p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
				# take action and upate board state
				prev_state = self.board
				self.updateState(p1_action)
				self.p1.feedReward(self.board,prev_state,0)
				# check board status if it is end

				win = self.winner()
				if win is not None:
					if show:
						self.showBoard()
						show = False
					# self.showBoard()
					# ended with p1 either win or draw
					self.giveReward(prev_state,True)
					self.reset()
					break

				else:
					# Player 2
					if show:
						self.showBoard()
					positions = self.availablePositions()
					p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
					self.updateState(p2_action)
					self.p1.feedReward(self.board,prev_state,0)

					win = self.winner()
					if win is not None:
						if show:
							self.showBoard()
							show = False
						# ended with p2 either win or draw
						self.giveReward(prev_state,True)
						self.reset()
						break
		return wins, state0

	# play with human
	def play2(self):
		while not self.isEnd:
			# Player 1
			self.showState(p1.check())
			positions = self.availablePositions()
			p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
			# take action and upate board state
			self.updateState(p1_action)
			self.showBoard()
			# check board status if it is end
			win = self.winner()
			if win is not None:
				self.reset()
				if win == 1:
					print(self.p1.name, "wins!")
				else:
					print("tie!")
				self.reset()
				break

			else:
				# Player 2
				positions = self.availablePositions()
				p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
				self.updateState(p2_action)
				self.showBoard()
				win = self.winner()
				if win is not None:
					if win == -1:
						print(self.p2.name, "wins!")
					else:
						print("tie!")
					self.reset()
					break
	
	def play3(self):
		while not self.isEnd:
			# Player 1
			positions = self.availablePositions()
			p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
			# take action and upate board state
			self.updateState(p1_action)
			win = self.winner()
			if win is not None:
				self.reset()
				if win == 1:
					return 1
				else:
					return 0
			else:
				# Player 2
				positions = self.availablePositions()
				p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
				self.updateState(p2_action)
				win = self.winner()
				if win is not None:
					self.reset()
					if win == -1:
						return -1
					else:
						return 0

	def showBoard(self):
		# p1: x  p2: o
		for i in range(0, BOARD_ROWS):
			print('-------------')
			out = '| '
			for j in range(0, BOARD_COLS):
				if self.board[i, j] == 1:
					token = 'x'
				if self.board[i, j] == -1:
					token = 'o'
				if self.board[i, j] == 0:
					token = ' '
				out += token + ' | '
			print(out)
		print('-------------')

	def showState(self,state):
		# p1: x  p2: o
		for i in range(0, BOARD_ROWS):
			print('-------------')
			out = '| '
			for j in range(0, BOARD_COLS):
				token = state[i*3+j][0][0]
				out += str(token) + ' | '
			print(out)
		print('-------------')


class Player:
	def __init__(self, name, exp_rate=0.8):
		self.name = name
		self.lr = 0.5
		self.model = self.create_model()
		self.exp_rate = exp_rate

	def create_model(self):
		model = Km.Sequential()
		model.add(Kl.Dense(18, activation='relu' ,input_dim=9))
		model.add(Kl.Dense(18, activation='relu'))
		model.add(Kl.Dense(1, activation='linear'))
		# optimzer is how do you want to minimise your loss function and admams is gradient descent with varying step size 
		model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
		model.summary()
		return model

	def chooseAction(self, positions, current_board, symbol):
		# possible actions
		PA = []
		if np.random.uniform(0, 1) <= self.exp_rate:
			# take random action
			idx = np.random.choice(len(positions))
			action = positions[idx]
		else:
			value_max = -999
			for p in positions:
				next_board = current_board.copy()
				next_board[p] = symbol
				value = self.calc_value(next_board)
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
		state = np.reshape(state,(1,9))
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
		prev_state = np.reshape(prev_state,(1,9))
		self.model.fit(prev_state, target, epochs=10, verbose=0)

	def savePolicy(self):
		self.model.save("/home/svu/e0235225/FYP/TicTacToe/Vmodel{}_6_v7".format(self.name))

	def loadPolicy(self, file):
		self.model = Km.load_model(file)

	def check(self):
		board1 = np.zeros((3,3))
		state_p1 = []
		actions = {'1':(0,0),'2':(0,1),'3':(0,2),'4':(1,0),'5':(1,1),'6':(1,2),'7':(2,0),'8':(2,1),'9':(2,2)}
		for i in range(1,10):
			board1[actions[str(i)]] = 1
			x = self.calc_value(board1)
			state_p1.append(x)
			board1 = np.zeros((3,3))
		return(state_p1)

class RandomPlayer:
	def __init__(self, name):
		self.name = name

	def chooseAction(self, positions, current_board, symbol):
		idx = np.random.choice(len(positions))
		action = positions[idx]
		return action

	# append a hash state
	def addState(self, state):
		pass

	# at the end of game, backpropagate and update states value
	def feedReward(self, reward):
		pass

	def reset(self):
		pass

class HumanPlayer:
	def __init__(self, name):
		self.name = name

	def chooseAction(self, positions, current_board, symbol):
		actions = {'1':(0,0),'2':(0,1),'3':(0,2),'4':(1,0),'5':(1,1),'6':(1,2),'7':(2,0),'8':(2,1),'9':(2,2)}
		while True:
			# row = int(input("Input your action row:"))
			# col = int(input("Input your action col:"))
			number = input("Input your move: ")
			try: 
				action = actions[number]
			except KeyError:
				continue
			if action in positions:
				return action

	# append a hash state
	def addState(self, state):
		pass

	# at the end of game, backpropagate and update states value
	def feedReward(self, reward):
		pass

	def reset(self):
		pass

if __name__ == "__main__":
	# training
	p1 = Player("p1")
	# p1.loadPolicy("/Users/admin/Desktop/Vmodelp1_6_v4")
	p2 = RandomPlayer("p2")
	st = State(p1, p2)
	print("training...")
	wins, state0 = st.play(10000)
	p1.savePolicy()
	fw = open('winsV_6_v7','wb')
	pickle.dump(wins, fw)
	fw.close()
	fw1 = open('statesV_6_v7','wb')
	pickle.dump(state0, fw1)
	fw1.close()

	# play with human
	# p1 = Player("computer", exp_rate=0)
	# p1.loadPolicy("/Users/admin/Desktop/Vmodelp1_6_v4")

	# p2 = HumanPlayer("human")
	
	# st = State(p1, p2)
	# st.play2()
