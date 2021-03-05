from ttt.player import Player
from ttt.game import Game
from ttt.ab_bot import AbBot
from ttt.human import Human
from ttt.vfunc_bot import VfuncBot
from datetime import datetime

def main():
    dateTimeObj = datetime.now()
    print(dateTimeObj)
    xbot = VfuncBot(Player.x,0)
    xbot.loadPolicy("/Users/admin/Desktop/po_Vmodel1_round5000/")
    # xbot = Human(Player.x)
    obot = AbBot(Player.o)
    game = Game(1,True)
    print ("vfuncbot (x) vs abbot (o)")
    game.simulate(xbot, obot)

    # xbot = InvinciBot(Player.x)
    # obot = AbBot(Player.o)
    # game = Game(15)
    # print ("invincibot (x) vs abbot (o)")
    # game.simulate(xbot, obot)

    
    dateTimeObj = datetime.now()
    print(dateTimeObj)

if __name__ == '__main__':
    main()