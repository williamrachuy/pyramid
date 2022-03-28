


import random, ui

from matplotlib.pyplot import table

SUITS = ('spades', 'hearts', 'clubs', 'diamonds')

def generateCards(card_type=['subjects', 'royals', 'jokers'], suit_type=['spades', 'hearts', 'clubs', 'diamonds']):

    ranks  = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'X']
    royals = ['J', 'Q', 'K']
    jokers = ['$']
    
    cards = []
    for suit in suit_type:
        if 'subjects' in card_type:
            for rank in ranks:
                cards.append(Card(rank, suit))
        if 'royals' in card_type:
            for royal in royals:
                cards.append(Card(royal, suit))
        if 'jokers' in card_type:
            for joker in jokers:
                cards.append(Card(joker, None))

    return cards

########################################################################################








class Card:

    def __init__(self, value=None, suit=None, visible=True, back=None):
        self.visible = visible
        self.value = value
        self.suit = suit
        self.back = back

    def flip(self):
        self.visible = not self.visible

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True
    
    def getFace(self):
        if self.visible:
            return ''.join((self.getValue(), self.getSuitChar()))
        else:
            return '??'

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit

    def getSuitChar(self):
        return self.suit[0].upper()









class Player:

    def __init__(self, name=None, house=None, score=0):
        self.name = name
        self.house = house
        self.score = score







class CardNode:
    def __init__(self, card_type=None, card=None):
        self.card = card
        self.card_type = card_type
    
    def setCard(self, card=None):
        self.card = card

    def getCard(self):
        return self.card

    def getFace(self):
        if self.card is None:
            return '[]'
        else:
            return self.card.getFace()



class GemNode:
    def __init__(self, card_node_left=None, card_node_right=None, card_node_center=None):
        self.gem = False
        self.card_node_left = card_node_left
        self.card_node_right = card_node_right
        self.card_node_center = card_node_center

    def setGem(self):
        self.gem = True

    def removeGem(self):
        self.gem = False

    def hasGem(self):
        if self.gem == True:
            return True
        return False



class Deck:

    def __init__(self, cards=[], hidden=True):
        self.cards = cards
        if hidden:
            self.hide()
    
    def draw(self, index=0, count=1):
        cards = []
        [cards.append(self.cards.pop(index)) for i in range(count)]
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def show(self):
        for card in self.cards:
            card.show()
        
    def hide(self):
        for card in self.cards:
            card.hide()



class Table:

    def __init__(self):
        self.deck = Deck(generateCards(card_type=['subjects'], suit_type=SUITS), hidden=False)
        self.deck.shuffle()
        self.houses = {
            'north' : House(suit='spades'),
            'east'  : House(suit='hearts'),
            'south' : House(suit='clubs'),
            'west'  : House(suit='diamonds')
        }

        self.card_nodes = {}
        self.setUpCardNodes()
        self.dealRoyals()
        self.dealSubjects()

        self.gem_nodes = {}
        self.setUpGemNodes()
        


    def setUpCardNodes(self):
        for card_type in ('royals', 'subjects'):
            self.card_nodes[card_type] = {}
            for suit in SUITS:
                self.card_nodes[card_type][suit] = {}
                for position in ('left', 'center', 'right'):
                    self.card_nodes[card_type][suit][position] = CardNode(card_type=card_type)

    def setUpGemNodes(self):
        for location in ('base', 'cap', 'court', 'peak'):
            self.gem_nodes[location] = {}

        for suit in SUITS:
            suit_next = SUITS[(SUITS.index(suit)+1) % len(SUITS)]
            dict_key_name = '{}-{}'.format(suit, suit_next)
            subjects = self.card_nodes['subjects'][suit]
            subjects_next = self.card_nodes['subjects'][suit_next]
            # base
            self.gem_nodes['base'][dict_key_name] = GemNode(card_node_left=subjects['right'], card_node_right=subjects_next['left'])
            # cap
            self.gem_nodes['cap'][dict_key_name] = GemNode(card_node_left=subjects['center'], card_node_right=subjects_next['center'])
            # court
            self.gem_nodes['court'][suit] = GemNode(card_node_left=subjects['left'], card_node_right=subjects['right'], card_node_center=subjects['center'])
        for suit in SUITS[0:2]:
            suit_next = SUITS[(SUITS.index(suit)+2) % len(SUITS)]
            dict_key_name = '{}-{}'.format(suit, suit_next)
            subjects = self.card_nodes['subjects'][suit]
            subjects_next = self.card_nodes['subjects'][suit_next]
            # peak
            self.gem_nodes['peak'][dict_key_name] = GemNode(card_node_left=subjects['center'], card_node_right=subjects_next['center'])

    
    def dealRoyals(self):
        for suit in SUITS:
            cards = generateCards(card_type=['royals'], suit_type=[suit])
            for position in ('left', 'center', 'right'):
                self.card_nodes['royals'][suit][position].setCard(cards.pop(0))

    def dealSubjects(self):
        for suit in SUITS:
            for position in ('left', 'center', 'right'):
                self.card_nodes['subjects'][suit][position].setCard(self.deck.draw()[0])



# class Pivot:

#     def __init__(self, card_a, card_b):
#         self.card_a = card_a
#         self.card_b = card_b

#     def pivot(self):
#         card_a = self.card_a
#         card_b = self.card_b
#         self.card_a = card_b
#         self.card_b = card_a



class House:

    def __init__(self, suit=None, position=None, hand=[], treasury=0):
        self.suit     = suit
        self.hand     = hand
        self.treasury = treasury
        # self.court = {
        #     'royals': {
        #         'left'  : None,
        #         'center': None,
        #         'right' : None
        #     },
        #     'subjects': {
        #         'left'  : None,
        #         'center': None,
        #         'right' : None
        #     }
        # }
        


########################################################################################



class Rules:
    # def __init__(self):
    #     pass

    def __init__(self, turn_order=SUITS):
        self.turn_order = turn_order

    # def getNextTurnSuit(self, turn_number):
    #     return self.turn_order[turn_number % len(self.turn_order) - 1]

    # def getActivePosition(self):


    def doesCardTrump(self, player_card, opponent_card):

        roy_trumps = [('K', 'Q'), ('Q', 'J'), ('J', 'K')]
        if (player_card.getValue(), opponent_card.getValue()) in roy_trumps:
            return True

        suit_trumps = [('spades', 'hearts'), ('hearts', 'clubs'), ('clubs', 'diamonds'), ('diamonds', 'spades')]
        if (player_card.getSuit(), opponent_card.getSuit()) in suit_trumps:
            if (opponent_card.getValue(), player_card.getValue()) in roy_trumps:
                return False
            return True
        
        return False

    def isPair(self, cards):
        if (cards[0].getValue() == cards[1].getValue()) or ('A' in (cards[0].getValue(), cards[1].getValue())):
            return True
        return False

    # def isFour(self, card_a, card_b, card_c, card_d):
    #     if (
    #             card_a.getValue() == card_b.getValue() and
    #             card_b.getValue() == card_c.getValue() and
    #             card_c.getValue() == card_d.getValue()
    #     ):
    #         return True
    #     return False

    def isFlush(self, suit, cards):
        for card in cards:
            if card.getSuit() != suit:
                return False
        return True



########################################################################################



class Game:

    def __init__(self):
        self.turn_number = 0
        self.table = Table()
        self.rules = Rules()

    def nextState(self):
        pass

    def generateGems(self):
        # base
        for suit_pair, gem_node in self.table.gem_nodes['base'].items():
            if self.rules.isPair(cards=(gem_node.card_node_left.getCard(), gem_node.card_node_right.getCard())):
                gem_node.setGem()
                print("gem set for base", suit_pair)
        # cap
        for suit_pair, gem_node in self.table.gem_nodes['cap'].items():
            if self.rules.isPair(cards=(gem_node.card_node_left.getCard(), gem_node.card_node_right.getCard())):
                gem_node.setGem()
                print("gem set for cap", suit_pair)
        # court
        for suit, gem_node in self.table.gem_nodes['court'].items():
            if self.rules.isFlush(suit=suit, cards=(gem_node.card_node_left.getCard(), gem_node.card_node_right.getCard(), gem_node.card_node_center.getCard())):
                gem_node.setGem()
                print("gem set for cour", suit)
        # peak
        empty = True
        for suit_pair, gem_node in self.table.gem_nodes['peak'].items():
            if gem_node.hasGem():
                empty = False
        for suit_pair, gem_node in self.table.gem_nodes['peak'].items():
            if (empty == True) and (self.rules.isPair(cards=(gem_node.card_node_left.getCard(), gem_node.card_node_right.getCard()))):
                gem_node.setGem()
                print("gem set for peak", suit_pair)
                empty = False



########################################################################################



if __name__ == '__main__':

    game = Game()
    # game loop here

    print(game.table.card_nodes['royals']['spades']['left'].getFace())



    '''
    rules = Rules()
    cards = generateCards(card_type='royals')
    for card_a in cards:
        for card_b in cards:
            if (card_a != card_b) and (card_a.getSuit() != card_b.getSuit()):
                print("{} -> {} ? {}".format(card_a.getFace(), card_b.getFace(), rules.doesCardTrump(card_a, card_b)))

    cards = generateCards(card_type='subjects')
    print("deck stuff")
    print("deck before", [card.getFace() for card in cards])
    deck = Deck(cards=cards)
    hand = deck.draw(index=4, count=3)
    print("deck after", [card.getFace() for card in cards])
    print("hand", [card.getFace() for card in hand])
    '''

    quit()


