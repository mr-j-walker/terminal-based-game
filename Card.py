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