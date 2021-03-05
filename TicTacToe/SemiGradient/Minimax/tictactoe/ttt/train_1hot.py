from .board import Board
from .player import Player
from .game import Game

class Train():
    def __init__(self, num_of_games):
        self.num_of_games = num_of_games
        self.game_wins = [[],[],[]]
        self.states = []
        self.moves = []
    
    def simulate(self, xbot, obot, print_game = False):
        for j in range(self.num_of_games):
            board = Board()
            current_turn = Player.x
            winner = None
            prev_board = board.grid
            if j % 1000 == 0:
                print_game = True
                print("Rounds {}".format(j))
                xbot_exp_rate = xbot.exp_rate
                xbot.exp_rate = 0
                test = Game(100)
                test.simulate(xbot,obot)
                if test.o_wins < 20:
                    xbot.exp_rate = xbot_exp_rate*0.9
                else:
                    xbot.exp_rate = xbot_exp_rate
                # here implicitly assumed that we always train the first player
                self.game_wins[0].append(test.o_wins)
                self.game_wins[1].append(test.ties)
                self.game_wins[2].append(test.x_wins)
                self.states.append(xbot.check(prev_board))
                if test.o_wins < 20:
                    xbot.savePolicy("/home/svu/e0235225/FYP/TicTacToe/1hotEpo_Vmodel1_round{}".format(str(j)))
                # print(self.states)
            for i in range(9):
                choice = []
                if (current_turn == xbot.player):
                    choice = xbot.select_move(board)
                else:
                    choice = obot.select_move(board)
                board.make_move(choice[0], choice[1], current_turn)

                winner = board.has_winner()

                if print_game:
                    self.moves.append(board.moves)
                    print_game = False
                if (winner != None):
                    #print ("Congrats " + str(winner))
                    break
                elif (i == 8):
                    #print ("It's a tie!")
                    break
                # here implicitly assumed that we always train the first player
                # and realised... we train twice for winning move in tictactoe_NN_vfunc6...
                if (current_turn == xbot.player):
                    xbot.feedReward(board.grid,prev_board,0)
                current_turn = current_turn.other
                prev_board = board.grid

            if (winner == Player.x):
                xbot.feedReward(board.grid,prev_board,2)
            elif (winner == Player.o):
                xbot.feedReward(board.grid,prev_board,-2)
            else:
                xbot.feedReward(board.grid,prev_board,1)
        