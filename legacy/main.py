import os, time
from game import Game, POSITIONS
from ui import UI

# test

if __name__ == '__main__':
    '''
    main should just be Game() and UI()
    '''
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
        ui.printTable(table=game.getTable())
        ui.printDeckSize(deck=game.table.getDeck())
        ui.printPlayers(players=game.getPlayers())
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
        elif user_input in ('draw', 'd'):
            game.players['player1'].draw(game.table.getDeck())
            game.players['player2'].draw(game.table.getDeck())
            game.players['player3'].draw(game.table.getDeck())
            game.players['player4'].draw(game.table.getDeck())
