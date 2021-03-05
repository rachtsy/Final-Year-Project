from .board import Board
from .player import Player
import pickle

class Game():
    def __init__(self, num_of_games, save_moves=False):
        self.num_of_games = num_of_games
        self.x_wins = 0
        self.o_wins = 0
        self.ties = 0
        self.moves = []
        self.save_moves = save_moves
    
    def simulate(self, xbot, obot, print_game = False):
        for j in range(self.num_of_games):
            board2 = Board()
            current_turn = Player.x
            winner = None
            for i in range(9):
                if i == 0 and self.save_moves == True:
                    self.moves.append(board2.moves)
                choice = []
                if (current_turn == xbot.player):
                    choice = xbot.select_move(board2)
                else:
                    choice = obot.select_move(board2)
                board2.make_move(choice[0], choice[1], current_turn)

                winner = board2.has_winner()

                if print_game:
                    board2.print()
                if (winner != None):
                    #print ("Congrats " + str(winner))
                    break
                elif (i == 8):
                    #print ("It's a tie!")
                    break
                current_turn = current_turn.other
            if (winner == Player.x):
                self.x_wins = self.x_wins + 1
            elif (winner == Player.o):
                self.o_wins = self.o_wins + 1
            else:
                self.ties = self.ties + 1
            if self.save_moves == True:
                fw2 = open('/Users/admin/Desktop/moves_{}'.format(str(j)),'wb')
                pickle.dump(self.moves, fw2)
                fw2.close()

        
        print ("x wins: " + str(self.x_wins))
        print ("o wins: " + str(self.o_wins))
        print ("ties: " + str(self.ties))