from ttt.player import Player
from ttt.game import Game
from ttt.human import Human
from ttt.vfunc_bot import VfuncBot
from ttt.ab_bot import AbBot
from datetime import datetime

def main():
    dateTimeObj = datetime.now()
    print(dateTimeObj)
    xbot = VfuncBot(Player.x,0)
    xbot.loadPolicy("/home/svu/e0235225/FYP/TicTacToe/AI")
    obot = Human(Player.o)
    # obot = AbBot(Player.o,0.3)
    game = Game(5,False)
    # print ("VfuncBot (x) vs Human (o)")
    game.simulate(xbot, obot, False)

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