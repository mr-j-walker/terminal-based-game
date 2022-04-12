# Terminal-Based Blackjack
This is a blackjack game between two players. 
## Gameplay Loop
+ At the start of the round: Player is asked if they want to play a round(costs $50 and is added to pot)
+ Each player(player, dealer) is then dealt a card, alternating, until they have 2 cards.
+ Only the last card in the dealer's hand is revealed
  + If the dealer has blackjack, it is revealed immediately and round ends.
+ The player will then decide how they want to play(hit, stand, fold)
  + If the player folds, they receieve half their bet back.
  + If the player hits, a card is added to their hand
    + If the value of the player's hand is equal to 21, the player is forced to stand.
    + If the value of the player's hand exceeds 21, they lose.
    + Otherwise, the player is offered a choice of what to do again.
  + If they stand, play is passed to the dealer.
+ Dealer will play similarly but has very specific rules it must follow.
  + If its hand is losing and has a value of 16 or less, it must hit.
  + If its hand has a value of 18 or more, it must stand.
+ Once the dealer ends its turn, scores are compared and pot is distributed

