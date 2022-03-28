import os, time
from game import Game
from ui import UI


if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()

    game = Game()
    ui = UI()

    quit = False
    while not quit:
        clear()
        ui.printSplash()
        # time.sleep(2)
        input()
        clear()
        game.__init__()
        game.generateGems()
        ui.printTable(table=game.table)
        if input("user> ").lower() in ('quit', 'exit', 'q'):
            quit = True
