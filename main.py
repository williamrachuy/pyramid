import os, time
from game import Game, POSITIONS
from ui import UI


if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()

    game = Game()
    ui = UI()

    clear()
    ui.printSplash()
    game.__init__()
    game.generateGems()
    input()
    quit = False
    pos_current = 0
    while not quit:
        # time.sleep(2)
        clear()
        ui.printTable(table=game.table)
        user_input = input("user> ").lower()
        if user_input in ('quit', 'exit', 'q'):
            quit = True
        elif user_input in ('pivot', 'p'):
            pos_next = (pos_current+1) % len(POSITIONS)
            # print(pos_current, pos_next)
            dict_key_name = '{}-{}'.format(POSITIONS[pos_current], POSITIONS[pos_next])
            pos_current = pos_next
            # print("attempting to pivot", dict_key_name)
            game.table.pivot_nodes['royals']['spades'][dict_key_name].pivot()

