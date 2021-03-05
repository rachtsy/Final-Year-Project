from ttt.player import Player
from ttt.train_1hot import Train
from ttt.vfunc_bot_1hot import VfuncBot
from ttt.ab_bot import AbBot
from datetime import datetime
import pickle

def main():
    dateTimeObj = datetime.now()
    print(dateTimeObj)
    xbot = VfuncBot(Player.x)
    obot = AbBot(Player.o,0.3)
    game = Train(20000)
    print ("Beginning training...")
    game.simulate(xbot, obot)
    
    dateTimeObj = datetime.now()
    print(dateTimeObj)

    xbot.savePolicy()
    fw = open('/home/svu/e0235225/FYP/TicTacToe/wins_EpoV1_v11','wb')
    pickle.dump(game.game_wins, fw)
    fw.close()
    fw1 = open('/home/svu/e0235225/FYP/TicTacToe/states_EpoV1_v11','wb')
    pickle.dump(game.states, fw1)
    fw1.close()
    fw2 = open('/home/svu/e0235225/FYP/TicTacToe/moves_EpoV1_v11','wb')
    pickle.dump(game.moves, fw2)
    fw2.close()


if __name__ == '__main__':
    main()