import random

class Card:

    suits = ["clubs", "spades", "hearts", "diamonds"]

    # this dictionary provides the value of face cards, for scoring purposes
    faces = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}

    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    #returns a quick discription of the card
    def __repr__(self):
        return "{face} of {suit}".format(face=self.face.title(), suit=self.suit.title())

class Deck:

    def __init__(self):
        self.pot = 0
        self.mainDeck = []
        # these nested loops generate a card for each face and suit and adds
        # them to the deck
        for suit in Card.suits:
            for face in Card.faces.keys():
                self.mainDeck.append(Card(suit, face))

    def __repr__(self):
        return "There are {} cards left in the deck.".format(len(self.mainDeck))

    # picks a random card from the deck, removes it and then returns it
    def drawCard(self):
        drawnCard = random.choice(self.mainDeck)
        self.mainDeck.remove(drawnCard)
        return drawnCard

    # deals cards to each player in an alternating fashion
    def dealCards(self, player, dealer):
        for i in range(2):
            player.drawCard(self)
            dealer.drawCard(self)

    # checks if the player's win conditions are met
    # then checks the dealer and resolves it there was a win, loss or tie
    def reportWin(self, player, dealer):
        player_win = (player.calcHand() > dealer.calcHand() or dealer.calcHand() > 21) and player.calcHand() <= 21
        dealer_win = (player.calcHand() < dealer.calcHand() or player.calcHand() > 21) and dealer.calcHand() <= 21
        if player_win and not dealer_win:
            return "{name} has won!".format(name=player.name)
        elif dealer_win and not player_win:
            return "The Dealer beat {name}!".format(name=player.name)
        return "{name} has tied with the Dealer!".format(name=player.name)

    # plays a round and asks player if they would like to play again
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

deck = Deck()
player = Player("")
dealer = Player("The Dealer", True)

player.name = input("What is your name?\n")
print("\n")
deck.playRound(player, dealer)
