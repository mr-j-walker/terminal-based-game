from Card import Card
from Deck import Deck

class Player:

    def __init__(self, name, ai=False):
        self.name = name
        self.hand = []
        self.ai = ai
        self.busted = False

    def __repr__(self):
        return "{name}, you have {count} left to play.".format(name=self.name, count=len(self.hand))

    # checks if the player in question has blackjack
    def hasBlackjack(self):
        if self.calcHand() == 21:
            self.printHand()
            print("{name} has blackjack!".format(name=self.name))
            return True
        return False
    # returns the value of the hand of the player instance
    # uses the lower value of an ace (1) if hand value is too high
    def calcHand(self):
        value = 0
        for card in self.hand:
            if not card.face == "ace":
                value += Card.faces[card.face]
        for card in self.hand:
            if card.face == "ace":
                if value + Card.faces[card.face] <= 21:
                    value += Card.faces[card.face]
                else:
                    value += 1
        if value > 21:
            self.busted = True
        return value
    
    # receives the passed card from drawCard() in deck and adds it to player's
    # hand
    def drawCard(self, deck):
        card = deck.drawCard()
        self.hand.append(card)
        return card

    # draws a card and checks if player instance has busted
    # returns false to break turn loop
    def hit(self, deck):
        print("{name} hit. They drew a(n) {card}\n".format(
            name=self.name, card=self.drawCard(deck)))

        if self.calcHand() > 21:
            self.busted = True
            print("{name} has {sum}, they have busted.\n".format(
                name=self.name, sum=self.calcHand()))
            return False
        return True

    # just prints that player decided to stand and
    # returns false to break turn loop
    def stand(self):
        print("{name} has {sum}, they decide to stand.\n".format(
            name=self.name, sum=self.calcHand()))
        return False

    #checks ai state of player instance so that ai players play accordding to
    #rules and non-ai players have a choice
    def control(self, other, deck):
        if self.ai:
            return self.decide(other, deck)
        else:
            return self.choose(deck)

    # this is the player's choice function, if the player has blackjack their
    # turn is ended immediately by returning False
    def choose(self, deck):
        prompt = """
        How would you like to play?
        1 - Hit
        2 - Stand
        """
        if not self.hasBlackjack():
            self.printHand()
            if not self.busted:
                pick = input(prompt)
                if pick == "1":
                    return self.hit(deck)
                elif pick == "2":
                    return self.stand()
                else:
                    print("Invalid Input!")
                    return self.choose(Deck)
        print("{name} has 21.".format(name=self.name))
        return False

    # this is the dealer's choice function, if the player has busted
    # then the loop is ended so that the dealer will win immediately
    def decide(self, other, deck):
        if not other.busted:
            self.printHand()
            if self.calcHand() <= 16 or not (self.calcHand() >= other.calcHand()):
                return self.hit(deck)
            elif self.calcHand() in range(18, 22):
                return self.stand()
        return False

    # prints the cards contained in player instance's hand 
    def printHand(self):
        print("{name}'s Hand:".format(name = self.name))
        for card in self.hand:
            print(card)
        print("Value: " + str(self.calcHand()) + "\n")

    # adds cards back to the deck and then resets players variables to defaults
    def reset(self, deck):
        deck.mainDeck += self.hand
        self.hand = []
        self.busted = False
