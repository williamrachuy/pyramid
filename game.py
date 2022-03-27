


import random, ui



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
        self.deck = Deck(generateCards(card_type=['subjects'], suit_type=['spades', 'hearts', 'clubs', 'diamonds']), hidden=False)
        self.deck.shuffle()
        self.houses = {
            'north' : House(suit='spades'),
            'east'  : House(suit='hearts'),
            'south' : House(suit='clubs'),
            'west'  : House(suit='diamonds')
        }

        self.setUpCardNodes()
        self.dealRoyals()
        self.dealSubjects()


    def setUpCardNodes(self):
        self.card_nodes = {}
        for card_type in ['royals', 'subjects']:
            self.card_nodes[card_type] = {}
            for suit in ['spades', 'hearts', 'clubs', 'diamonds']:
                self.card_nodes[card_type][suit] = {}
                for position in ['left', 'center', 'right']:
                    self.card_nodes[card_type][suit][position] = CardNode(card_type=card_type)
    
    def dealRoyals(self):
        for suit in ['spades', 'hearts', 'clubs', 'diamonds']:
            cards = generateCards(card_type=['royals'], suit_type=[suit])
            for position in ['left', 'center', 'right']:
                self.card_nodes['royals'][suit][position].setCard(cards.pop(0))

    def dealSubjects(self):
        for suit in ['spades', 'hearts', 'clubs', 'diamonds']:
            for position in ['left', 'center', 'right']:
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
        self.court = {
            'royals': {
                'left'  : None,
                'center': None,
                'right' : None
            },
            'subjects': {
                'left'  : None,
                'center': None,
                'right' : None
            }
        }
        


########################################################################################



class Rules:
    # def __init__(self):
    #     pass

    def __init__(self, turn_order=['spades', 'hearts', 'clubs', 'diamonds']):
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

    def isPair(self, card_a, card_b):
        if card_a.getValue() == card_b.getValue():
            return True
        return False

    def isFour(self, card_a, card_b, card_c, card_d):
        if (
                card_a.getValue() == card_b.getValue() and
                card_b.getValue() == card_c.getValue() and
                card_c.getValue() == card_d.getValue()
        ):
            return True
        return False

    def isFlush(self, court):
        if (
                court.roy_l.getSuit() == court.roy_m.getSuit() and
                court.roy_m.getSuit() == court.roy_r.getSuit() and
                court.roy_r.getSuit() == court.num_l.getSuit() and
                court.num_l.getSuit() == court.num_m.getSuit() and
                court.num_m.getSuit() == court.num_r.getSuit()
        ):
            return True
        return False



########################################################################################



class Game:

    def __init__(self):
        self.turn_number = 0
        self.table = Table()

    def nextState():
        pass



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


