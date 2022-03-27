
class UI():

    def printTable(self, table):
        empty = '[]'
        table_chars = [
           #'  ..  ..  ..  ..  ..  ..  ..  '
            '                              ',
            '          {}  {}  {}          '.format(table.card_nodes['royals']['clubs']['right'].getFace(), table.card_nodes['royals']['clubs']['center'].getFace(), table.card_nodes['royals']['clubs']['left'].getFace()),
            '                              ',
            '      {}  {}  {}  {}  {}      '.format(empty, table.card_nodes['subjects']['clubs']['right'].getFace(), empty, table.card_nodes['subjects']['clubs']['left'].getFace(), empty),
            '                              ',
            '  {}  {}  {}  {}  {}  {}  {}  '.format(table.card_nodes['royals']['diamonds']['left'].getFace(), table.card_nodes['subjects']['diamonds']['left'].getFace(), empty, table.card_nodes['subjects']['clubs']['center'].getFace(), empty, table.card_nodes['subjects']['hearts']['right'].getFace(), table.card_nodes['royals']['hearts']['right'].getFace()),
            '                              ',
            '  {}  {}  {}  {}  {}  {}  {}  '.format(table.card_nodes['royals']['diamonds']['center'].getFace(), empty, table.card_nodes['subjects']['diamonds']['center'].getFace(), empty, table.card_nodes['subjects']['hearts']['center'].getFace(), empty, table.card_nodes['royals']['hearts']['center'].getFace()),
            '                              ',
            '  {}  {}  {}  {}  {}  {}  {}  '.format(table.card_nodes['royals']['diamonds']['right'].getFace(), table.card_nodes['subjects']['diamonds']['right'].getFace(), empty, table.card_nodes['subjects']['spades']['center'].getFace(), empty, table.card_nodes['subjects']['hearts']['left'].getFace(), table.card_nodes['royals']['hearts']['left'].getFace()),
            '                              ',
            '      {}  {}  {}  {}  {}      '.format(empty, table.card_nodes['subjects']['spades']['left'].getFace(), empty, table.card_nodes['subjects']['spades']['right'].getFace(), empty),
            '                              ',
            '          {}  {}  {}          '.format(table.card_nodes['royals']['spades']['left'].getFace(), table.card_nodes['royals']['spades']['center'].getFace(), table.card_nodes['royals']['spades']['right'].getFace()),
            '                              ',
           #'  ..  ..  ..  ..  ..  ..  ..  '
        ]
        
        for row in table_chars:
            print(row)