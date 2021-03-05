class Human():
	def __init__(self, player):
		self.player = player

	def select_move(self, board):
		positions = board.get_legal_moves()
		board.print()
		actions = {'1':[0,0],'2':[0,1],'3':[0,2],'4':[1,0],'5':[1,1],'6':[1,2],'7':[2,0],'8':[2,1],'9':[2,2]}
		while True:
			number = input("Input your move: ")
			try: 
				action = actions[number]
			except KeyError:
				continue
			if action in positions:
				return action