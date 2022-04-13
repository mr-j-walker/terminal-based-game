import random

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
        self.pot = 0
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

    def report_win(self, player, dealer):
        player_win = player.sum > dealer.sum and player.sum <= 21
        if player_win or dealer.sum > 21:
            return "{name} has won!".format(name=player.name)
        elif not player_win and player.sum == dealer.sum:
            player.money += player.bet
            dealer.money += dealer.bet
            return "{name} has tied with the Dealer!".format(name = player.name)
        return "The Dealer beat {name}!".format(name = player.name)

    def start_round(self, player, dealer):
        deck.takeBet(player)
        deck.takeBet(dealer)
        for i in range(2):
            player.draw_card(self)
            dealer.draw_card(self)
        print("Dealer has a {card}".format(card=dealer.hand[-1]))

        while(not player.decide(dealer, deck)):
            pass

        while(not dealer.decide(player, deck)):
            pass

        print(self.report_win(player, dealer))

class Player:

    def __init__(self, name, ai = False):   
        self.name = name
        self.hand = []
        self.money = 3000
        self.sum = 0
        self.ai = ai
        self.bet = 50
        self.busted = False
    
    def __repr__(self):
        return "{name}, you have {money} left to play.".format(name = self.name, money = self.money)

    def betMoney(self):
        
        self.money -= self.bet
        return self.bet

    def draw_card(self, deck):
        card = deck.drawCard()
        self.hand.append(card)
        self.sum += Card.faces[card.face]

    def hit(self, deck):
        print("{name} has {sum}, they hit.".format(name=self.name, sum = self.sum))
        self.draw_card(deck)
        if self.sum > 21:
            self.busted = True
            print("{name} has {sum}, they have busted.".format(name=self.name, sum = self.sum))
            return True
        print("{name} now has {sum}".format(name=self.name, sum = self.sum))
        return False

    def stand(self):
        print("{name} has {sum}, they decide to stand.".format(name=self.name, sum = self.sum))
        return True

    def fold(self):
        print("{name} has decided to fold.".format(name=self.name))
        return True

    def decide(self, other, deck):
        if not other.busted:
            # if self.ai:
            if self.sum <= 16 or not (self.sum >= other.sum):
                return self.hit(deck)
            elif self.sum in range(18, 22):
                return self.stand()
        return self.stand()

    def reset(self, deck):
        deck.mainDeck += self.hand
        self.hand = []
        self.sum = 0
        self.busted = False


deck = Deck()
player = Player("Greg")
dealer = Player("The Dealer", True)

deck.start_round(player, dealer)
