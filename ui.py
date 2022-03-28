'''
'  ..  ..  ..  ..  ..  ..  ..  '
'                              '
'          {}  {}  {}          '
'                              '
'      {}  {}  {}  {}  {}      '
'                              '
'  {}  {}  {}  {}  {}  {}  {}  '
'                              '
'  {}  {}  {}  {}  {}  {}  {}  '
'                              '
'  {}  {}  {}  {}  {}  {}  {}  '
'                              '
'      {}  {}  {}  {}  {}      '
'                              '
'          {}  {}  {}          '
'                              '
'  ..  ..  ..  ..  ..  ..  ..  '
'''


SPLASH = [
    '.....................................:!7^.......................................',
    '...................................:!YY??7^.....................................',
    '.................................:75P5J7?YJ7~:..................................',
    '...............................:7Y5555J7J?JJ?!~.................................',
    '.............................:JPPPP55PY?JJJ??JY?~...............................',
    '...........................~J5GGPPPGGBP555YYY555PY!:............................',
    ':::::::::::::::::::::::.:~JPPPPPPPGPPPYJJJJYJJJYY55J!:...........::.............',
    '!!77!!!!!!!!!!!!!!!!!!7?YPPPPPPPPPPPP5JJJJJJJJJYYYYYYJ?!!!!!!!!!!77!!!!!!!!!!!!!',
    '?7?7!!!!!!!!!!!!!!!!7?5P555PPPPPPPP5PYJJJJJJYYYYYYYYYYYJ?7!!77777777777777777777',
    '777777777777777777?YPP555PPPPGGGGGGGPJJJJJJJJYYYYJYYYJJJJJ77!7777777777777777777',
    '777?7?????????7?J5PGPPPPPPGGGGGGGGGGBYJJYYYYYJYYYYYYYJJJJJJYJ7777777777777777777',
    '7?77777?777777J5PGGPPPGGGGGGGGGPGPPBP555YYYYYJY55YYY5YYJYY555YY?7777777777777777',
    '777777777777YPGPPPGGGGGGGGGGGPPGGPGBP55YYY55YYYY5555555YYY555555Y?77777777777777',
    'JJYJ?????Y5GBBGGGGGGGGGGGGGGGGGGGGBG5555YYY5555555555P555PP5555PPP5?7777777!7777',
    '7777!!!JPB    ____,  _  _,  ____,    ____,  __, _,  __,   ____,   5PY??77?????7?',
    '!!!~!?PBBG   (-|__) (-\_/  (-|__)   (-/_|  (-|\/|  (-|   (-|  \   5555Y7!!777?7?',
    '^^!JGBBGGG    _|      _|,   _|  \,  _/  |,  _| _|,  _|_,  _|__/   5Y5Y55Y?~~!!~~',
    '7YGBBGGGGG                                                        5555Y55P5J!~~~',
    'PPPPGGGGGGGGGGGGGGGGGGGGGGGGGGGBBBPP55555555555555P55555P555555555555YY55Y55YJ!~',
    '555P55PPPPPPPPPGGGGGGGGGGGGGGGGGBBPP5YYYY5P5P555555YY5YY55YYY5YYYYYYYJ?J?777777!',
    '5555P555P5PP5P5PPPPPPPGGGGGGGGGBBGP5YYYYY555Y5YJ?J?J?7?77!!?!!77!7!~!7?7~~~~~^~~',
    '5555555555555555555555PPPPP5PPPPP5JJ??7?77777?J?!7!~~~~!~~~~~!!~~~~~~~~~~~~~~~~~'
]


class UI():

    def convert(self, test, char_true, char_false='??'):
        if test:
            return char_true
        return char_false
        
    def printSplash(self):
        for row in SPLASH:
            print(row)

    def printTable(self, table):
        empty = '--'
        gem = '$$'
        table_chars = [
           #'  ..  ..  ..  ..  ..  ..  ..  '
           r'                              ',
           r'          {}  {}  {}          '.format(table.card_nodes['royals']['clubs']['right'].getFace(), table.card_nodes['royals']['clubs']['center'].getFace(), table.card_nodes['royals']['clubs']['left'].getFace()),
           r'                              ',
           r'      {}  {}  {}  {}  {}      '.format(self.convert(test=table.gem_nodes['base']['clubs-diamonds'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['clubs']['right'].getFace(), self.convert(test=table.gem_nodes['court']['clubs'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['clubs']['left'].getFace(), self.convert(test=table.gem_nodes['base']['hearts-clubs'].hasGem(), char_true=gem, char_false=empty)),
           r'                              ',
           r'  {}  {}  {}  {}  {}  {}  {}  '.format(table.card_nodes['royals']['diamonds']['left'].getFace(), table.card_nodes['subjects']['diamonds']['left'].getFace(), self.convert(test=table.gem_nodes['cap']['clubs-diamonds'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['clubs']['center'].getFace(), self.convert(test=table.gem_nodes['cap']['hearts-clubs'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['hearts']['right'].getFace(), table.card_nodes['royals']['hearts']['right'].getFace()),
           r'                              ',
           r'  {}  {}  {}  {}  {}  {}  {}  '.format(table.card_nodes['royals']['diamonds']['center'].getFace(), self.convert(test=table.gem_nodes['court']['diamonds'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['diamonds']['center'].getFace(), self.convert(test=table.gem_nodes['peak']['spades-clubs'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['hearts']['center'].getFace(), self.convert(test=table.gem_nodes['court']['hearts'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['royals']['hearts']['center'].getFace()),
           r'                              ',
           r'  {}  {}  {}  {}  {}  {}  {}  '.format(table.card_nodes['royals']['diamonds']['right'].getFace(), table.card_nodes['subjects']['diamonds']['right'].getFace(), self.convert(test=table.gem_nodes['cap']['diamonds-spades'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['spades']['center'].getFace(), self.convert(test=table.gem_nodes['cap']['spades-hearts'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['hearts']['left'].getFace(), table.card_nodes['royals']['hearts']['left'].getFace()),
           r'                              ',
           r'      {}  {}  {}  {}  {}      '.format(self.convert(test=table.gem_nodes['base']['diamonds-spades'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['spades']['left'].getFace(), self.convert(test=table.gem_nodes['court']['spades'].hasGem(), char_true=gem, char_false=empty), table.card_nodes['subjects']['spades']['right'].getFace(), self.convert(test=table.gem_nodes['base']['spades-hearts'].hasGem(), char_true=gem, char_false=empty)),
           r'                              ',
           r'          {}  {}  {}          '.format(table.card_nodes['royals']['spades']['left'].getFace(), table.card_nodes['royals']['spades']['center'].getFace(), table.card_nodes['royals']['spades']['right'].getFace()),
           r'                             ',
           #'  ..  ..  ..  ..  ..  ..  ..  '
        ]
        
        for row in table_chars:
            print(row)