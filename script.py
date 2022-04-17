import random


class Card:

    suits = ["clubs", "spades", "hearts", "diamonds"]
    faces = {"ace": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "jack": 10, "queen": 10, "king": 10}

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
        player_win = player.sum > dealer.sum and player.sum <= 21
        dealer_win = (player.sum < dealer.sum or player.sum > 21) and dealer.sum <= 21
        if player_win and not dealer_win:
            return "{name} has won!".format(name=player.name)
        elif dealer_win and not player_win:
            return "The Dealer beat {name}!".format(name=player.name)
        return "{name} has tied with the Dealer!".format(name=player.name)


    def playRound(self, player, dealer):
        self.dealCards(player, dealer)
        print("Dealer has a {card}".format(card=dealer.hand[-1]))

        while(player.control(dealer, deck)):
            pass

        while(dealer.decide(player, deck)):
            pass

        print(self.reportWin(player, dealer))


class Player:

    def __init__(self, name, ai=False):
        self.name = name
        self.hand = []
        self.sum = 0
        self.ai = ai
        self.busted = False

    def __repr__(self):
        return "{name}, you have {count} left to play.".format(name=self.name, count=len(self.hand))

    def drawCard(self, deck):
        card = deck.drawCard()
        self.hand.append(card)
        self.sum += Card.faces[card.face]

    def hit(self, deck):
        print("{name} has {sum}, they hit.".format(
            name=self.name, sum=self.sum))
        self.drawCard(deck)
        if self.sum > 21:
            self.busted = True
            print("{name} has {sum}, they have busted.".format(
                name=self.name, sum=self.sum))
            return False
        print("{name} now has {sum}".format(name=self.name, sum=self.sum))
        return True

    def stand(self):
        print("{name} has {sum}, they decide to stand.".format(
            name=self.name, sum=self.sum))
        return False

    def fold(self):
        print("{name} has decided to fold.".format(name=self.name))
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
        2 - Stand
        3 - Fold (1/2 of your bet is returned)\n
        """
        print("Your Hand:\n")
        for card in self.hand:
            print(card)
        if not self.busted:
            pick = input(prompt)
            if pick == "1":
                return self.hit(deck)
            elif pick == "2":
                return self.stand()
            elif pick == "3":
                return self.fold()
            else:
                print("Invalid Input!")
                return self.choose(Deck)
        return False

    def decide(self, other, deck):
        if not other.busted:
            if self.sum <= 16 or not (self.sum >= other.sum):
                return self.hit(deck)
            elif self.sum in range(18, 22):
                return self.stand()
        return False

    def reset(self, deck):
        deck.mainDeck += self.hand
        self.hand = []
        self.sum = 0
        self.busted = False


deck = Deck()
player = Player(" ")
dealer = Player("The Dealer", True)

player.name = input("What is your name?\n")

deck.playRound(player, dealer)
