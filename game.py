


import random



def generateCards(card_type=['ranks', 'royals', 'jokers'], suit_type=['S', 'H', 'C', 'D']):
    ranks  = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    royals = ['J', 'Q', 'K']
    jokers = ['$']
    
    cards = []
    for suit in suit_type:
        if 'ranks' in card_type:
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
        return (self.value, self.suit)

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit



class Player:

    def __init__(self, name=None, house=None):
        self.name = name
        self.house = house



class Node:

    def __init__(self, position=None, treasure=False, type=None):
        self.position = position
        self.treasure = treasure
        self.type = type

    def generatetreasure(self):
        self.treasure = True

    def removetreasure(self):
        self.treasure = False

    def pivot(self, card_a, card_b):
        pass


class Deck:

    def __init__(self, cards=[]):
        self.cards = cards
    
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

    def __init__(self, deck=Deck()):
        self.deck = deck        
        self.houses = {
            'north' : House(suit='S'),
            'east'  : House(suit='H'),
            'south' : House(suit='C'),
            'west'  : House(suit='D')
        }
        # self.pivots = {}
        # for position in ['north', 'east', 'south', 'west']:
        #     for title in ['royals', 'subjects', 'opponents']:
        #         if title == 'opponents':
        #             for lane in ['left', 'middle', 'right']:
        #                 self.pivots
        #         else:
                    


        self.nodes = {
            'northeast' : Node(position='northeast'),
            'southeast' : Node(position='southeast'),
            'southwest' : Node(position='southwest'),
            'northwest' : Node(position='northwest'),
            'center'    : Node(position='center'),
            'north'     : Node(position='north'),
            'east'      : Node(position='east'),
            'south'     : Node(position='south'),
            'west'      : Node(position='west')
        }



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
                'middle': None,
                'right' : None
            },
            'subjects': {
                'left'  : None,
                'middle': None,
                'right' : None
            }
        }
        


########################################################################################



class Rules:
    # def __init__(self):
    #     pass

    def __init__(self, turn_order=['S', 'H', 'C', 'D']):
        self.turn_order = turn_order

    # def getNextTurnSuit(self, turn_number):
    #     return self.turn_order[turn_number % len(self.turn_order) - 1]

    # def getActivePosition(self):


    def doesCardTrump(self, player_card, opponent_card):

        roy_trumps = [('K', 'Q'), ('Q', 'J'), ('J', 'K')]
        if (player_card.getValue(), opponent_card.getValue()) in roy_trumps:
            return True

        suit_trumps = [('S', 'H'), ('H', 'C'), ('C', 'D'), ('D', 'S')]
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

    def nextState():
        pass



########################################################################################



if __name__ == '__main__':

    game = Game()


    '''
    rules = Rules()
    cards = generateCards(card_type='royals')
    for card_a in cards:
        for card_b in cards:
            if (card_a != card_b) and (card_a.getSuit() != card_b.getSuit()):
                print("{} -> {} ? {}".format(card_a.getFace(), card_b.getFace(), rules.doesCardTrump(card_a, card_b)))

    cards = generateCards(card_type='ranks')
    print("deck stuff")
    print("deck before", [card.getFace() for card in cards])
    deck = Deck(cards=cards)
    hand = deck.draw(index=4, count=3)
    print("deck after", [card.getFace() for card in cards])
    print("hand", [card.getFace() for card in hand])
    '''

    quit()


