from Card import Card
from Deck import Deck
from Player import Player

# This is where the program is started
deck = Deck()
player = Player(input("What is your name?\n"))
dealer = Player("The Dealer", True)
deck.playRound(player, dealer, deck)
