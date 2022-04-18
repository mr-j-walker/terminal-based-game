import random
from Card import Card

class Deck:

    def __init__(self):
        self.pot = 0
        self.mainDeck = []
        # these nested loops generate a card for each face and suit and adds
        # them to the deck
        for suit in Card.suits:
            for face in Card.faces.keys():
                self.mainDeck.append(Card(suit, face))
        random.shuffle(self.mainDeck)
        
    def __repr__(self):
        return "There are {} cards left in the deck.".format(len(self.mainDeck))

    def shuffle(self):
        random.shuffle(self.mainDeck)

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
    def playRound(self, player, dealer, deck):
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
            if choice:
                player.reset(deck)
                dealer.reset(deck)
                self.shuffle()