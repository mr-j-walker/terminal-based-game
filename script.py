import random
from unicodedata import name

class Card:
    
    suits = ["clubs", "spades", "hearts", "diamonds"]
    faces = {"ace": 1, "two" : 2, "three" : 3, "four" : 4, "five" : 5, "six" : 6, "seven" : 7, "eight" : 8, "nine": 9, "ten" : 10 , "jack" : 10, "queen" : 10, "king" : 10}

    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __repr__(self):
        return "{face} of {suit}".format(face = self.face.title(), suit = self.suit.title())

class Deck:

    def __init__(self):
        pot = 0
        self.mainDeck = []
        for suit in Card.suits:
            for face in Card.faces.keys():
                self.mainDeck.append(Card(suit, face))

    def __repr__(self):
        return "There are {} cards left in the deck.".format(len(self.mainDeck))
    
    def takeBet(self, player):
        self.pot += player.betMoney()
    
    def drawCard(self):
        drawnCard = random.choice(self.mainDeck)
        self.mainDeck.remove(drawnCard)
        return drawnCard

    def start_round(self, player, dealer):
        player.betMoney()
        dealer.betMoney()
        for i in range(2):
            player.draw_card(self)
            dealer.draw_card(self)
        print("Dealer has a {card}".format(card=dealer.hand[-1]))

        while(not player.play_round(dealer, deck)):
            pass

        while(not dealer.play_round(player, deck)):
            pass
        # player.

    def is_win(self, other):
        win = self.sum > other.sum and self.sum <= 21
        if win:
            print("{name} with {sum} beat ")
        return win

class Player:

    def __init__(self, name, ai = False):   
        self.name = name
        self.hand = []
        self.money = 3000
        self.sum = 0
        self.ai = ai
    
    def __repr__(self):
        return "{name}, you have {money} left to play.".format(name = self.name, money = self.money)

    def betMoney(self):
        bet = 30
        self.money -= bet
        return bet

    def draw_card(self, deck):
        card = deck.drawCard()
        self.hand.append(card)
        self.sum += Card.faces[card.face]

    def play_round(self, other, deck):
        if self.sum > 21:
            print("{name} has {sum}, they have busted.".format(name=self.name, sum = self.sum))
            return True
        elif self.sum < 18 and self.sum < other.sum:
            print("{name} has {sum}, they hit.".format(name=self.name, sum = self.sum))
            self.draw_card(deck)
            print("{name} now has {sum}".format(name=self.name, sum = self.sum))
            return False
        print("{name} has {sum}, they decide to stand.".format(name=self.name, sum = self.sum))
        return True

    def reset(self, deck):
        deck.mainDeck += self.hand
        self.__init__(self.name, self.ai)
        pass

deck = Deck()
player = Player("Greg")
dealer = Player("The Dealer", True)

deck.start_round(player, dealer)
