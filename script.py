import random

class Player:
    
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.money = 3000
        self.sum
    
    def __repr__(self):
        return "{name} has {money} left to play.".format(name = self.name, money = self.money)

    def draw_card(self, deck):
        self.hand.append(deck.drawCard())

class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __repr__(self):
        return "{face} of {suit}".format(face = self.face.title(), suit = self.suit.title())
    

class Deck:
    suits = ["clubs", "spades", "hearts", "diamonds"]
    faces = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king"]

    def __init__(self):
        self.mainDeck = []
        for suit in self.suits:
            for face in self.faces:
                self.mainDeck.append(Card(suit, face))

    def __repr__(self):
        return "There are {} cards left in the deck.".format(len(self.mainDeck))
    
    def drawCard(self):
        return random.choice(self.mainDeck)

def main_loop():
    player = Player("Greg")
    dealer = Player("The Dealer")

    
    