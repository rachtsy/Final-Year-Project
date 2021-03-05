from ttt.player import Player
from ttt.game import Game
from ttt.vfunc_bot import VfuncBot
from ttt.random_bot import RandomBot
from ttt.ab_bot import AbBot
from datetime import datetime

def main():
    dateTimeObj = datetime.now()
    print(dateTimeObj)
    xbot = VfuncBot(Player.x,0)
    xbot.loadPolicy("/Users/admin/Desktop/tttV/TicTacToeV_6/v7/Vmodelp1_6_v7/")
    obot = RandomBot(Player.o)
    game = Game(5,True)
    print ("VfuncBot (x) vs randombot (o)")
    game.simulate(xbot, obot, True)

    # xbot = RandomBot(Player.x)
    # obot = AbBot(Player.o)
    # game = Game(15)
    # print ("randombot (x) vs abbot (o)")
    # game.simulate(xbot, obot)

    # xbot = AbBot(Player.x)
    # obot = AbBot(Player.o)
    # game = Game(15)
    # print ("abbot (x) vs abbot (o)")
    # game.simulate(xbot, obot)
    
    dateTimeObj = datetime.now()
    print(dateTimeObj)

if __name__ == '__main__':
    main()