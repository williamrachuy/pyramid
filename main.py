from game import Game
from ui import UI

if __name__ == '__main__':
    game = Game()
    # game loop here

    ui = UI()

    ui.printTable(table=game.table)
