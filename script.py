import random

class Card:
 
    suits = ["clubs", "spades", "hearts", "diamonds"]
    faces = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}

    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __repr__(self):
        return "{face} of {suit}".format(face=self.face.title(), suit=self.suit.title())

class Deck:

    def __init__(self):
        self.pot = 0
        self.mainDeck = []
        for suit in Card.suits:
            for face in Card.faces.keys():
                self.mainDeck.append(Card(suit, face))

    def __repr__(self):
        return "There are {} cards left in the deck.".format(len(self.mainDeck))

    def drawCard(self):
        drawnCard = random.choice(self.mainDeck)
        self.mainDeck.remove(drawnCard)
        return drawnCard

    def dealCards(self, player, dealer):
        for i in range(2):
            player.drawCard(self)
            dealer.drawCard(self)

    def reportWin(self, player, dealer):
        player_win = (player.calcHand() > dealer.calcHand() or dealer.calcHand() > 21) and player.calcHand() <= 21
        dealer_win = (player.calcHand() < dealer.calcHand() or player.calcHand() > 21) and dealer.calcHand() <= 21
        if player_win and not dealer_win:
            return "{name} has won!".format(name=player.name)
        elif dealer_win and not player_win:
            return "The Dealer beat {name}!".format(name=player.name)
        return "{name} has tied with the Dealer!".format(name=player.name)

    def playRound(self, player, dealer):
        choice = True
        while choice:
            self.dealCards(player, dealer)
            print("Dealer has a(n) {card}\n".format(card=dealer.hand[-1]))

            while((not player.hasBlackjack()) and player.control(dealer, deck)):
                pass

            while((not dealer.hasBlackjack()) and dealer.control(player, deck)):
                pass

            print(self.reportWin(player, dealer))
            choice = input("\nWould you like to play again? (y/n)\n") == "y"
            player.reset(deck)
            dealer.reset(deck)

class Player:

    def __init__(self, name, ai=False):
        self.name = name
        self.hand = []
        self.ai = ai
        self.busted = False

    def __repr__(self):
        return "{name}, you have {count} left to play.".format(name=self.name, count=len(self.hand))

    def hasBlackjack(self):
        if self.calcHand() == 21:
            print("{name} has blackjack!".format(name=self.name))
            return True
        return False

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

    def drawCard(self, deck):
        card = deck.drawCard()
        self.hand.append(card)
        return card

    def hit(self, deck):
        print("{name} hit. They drew a(n) {card}\n".format(
            name=self.name, card=self.drawCard(deck)))

        if self.calcHand() > 21:
            self.busted = True
            print("{name} has {sum}, they have busted.\n".format(
                name=self.name, sum=self.calcHand()))
            return False
        return True

    def stand(self):
        print("{name} has {sum}, they decide to stand.\n".format(
            name=self.name, sum=self.calcHand()))
        return False

    def control(self, other, deck):
        if self.ai:
            return self.decide(other, deck)
        else:
            return self.choose(deck)

    def choose(self, deck):
        prompt = """
        How would you like to play?
        1 - Hit
        2 - Stand\n
        """
        if not self.calcHand == 21:
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

    def decide(self, other, deck):
        if not other.busted:
            self.printHand()
            if self.calcHand() <= 16 or not (self.calcHand() >= other.calcHand()):
                return self.hit(deck)
            elif self.calcHand() in range(18, 22):
                return self.stand()
        return False

    def printHand(self):
        print("{name}'s Hand:".format(name = self.name))
        for card in self.hand:
            print(card)
        print("Value: " + str(self.calcHand()) + "\n")

    def reset(self, deck):
        deck.mainDeck += self.hand
        self.hand = []
        self.busted = False

deck = Deck()
player = Player("")
dealer = Player("The Dealer", True)

player.name = input("What is your name?\n")
print("\n")
deck.playRound(player, dealer)
