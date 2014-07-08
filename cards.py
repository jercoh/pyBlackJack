import random

SUITLIST = ('heart', 'diamond', 'spade', 'club')
RANKLIST = ('A ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ',
            '8 ', '9 ', '10', 'J ', 'Q ', 'K ')
VALUEMAP = {'A ':1, '2 ':2, '3 ':3, '4 ':4, '5 ':5,
            '6 ':6, '7 ':7, '8 ':8, '9 ':9, '10':10,
            'J ':10, 'Q ':10, 'K ':10}
TOP = " _______"
BOTTOM = "|_____"

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

    def validSuits():
        return SUITLIST

    def getSuit(self):
        return self.suit

    def getRank(self):
        return self.rank

    def getValue(self):
        return VALUEMAP[self.rank]

class AsciiArtCard(Card):
    def __init__(self, rank, suit):
        Card.__init__(self, rank, suit)
        self.top_line = TOP
        if self.getSuit() == "spade":
            self.first_line = "|"+self.getRank()+" .   |"
            self.second_line = "|  /.\  |"
            self.third_line = "| (_._) |"
            self.fourth_line = "|   |   |"
        elif self.getSuit() == "club":
            self.first_line = "|"+self.getRank()+" _   |"
            self.second_line = "|  ( )  |"
            self.third_line = "| (_'_) |"
            self.fourth_line = "|   |   |"
        elif self.getSuit() == "heart":
            self.first_line = "|"+self.getRank()+"_ _  |"
            self.second_line = "| ( v ) |"
            self.third_line = "|  \ /  |"
            self.fourth_line = "|   .   |"
        elif self.getSuit() == "diamond":
            self.first_line = "|"+self.getRank()+" .   |"
            self.second_line = "|  / \  |"
            self.third_line = "|  \ /  |"
            self.fourth_line = "|   v   |"
        self.bottom_line = BOTTOM+self.getRank()+"|"

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        result = ""
        for card in self.cards:
            result += card.top_line+"   "
        result += "\n"
        for card in self.cards:
            result += card.first_line+"  "
        result += "\n"
        for card in self.cards:
            result += card.second_line+"  "
        result += "\n"
        for card in self.cards:
            result += card.third_line+"  "
        result += "\n"
        for card in self.cards:
            result += card.fourth_line+"  "
        result += "\n"
        for card in self.cards:
            result += card.bottom_line+"  "
        result += "\n"
        return result

    def deal(self, card):
        self.cards.append(card)

    def getValue(self):
        value = 0
        for card in self.cards:
            value += card.getValue()
        for card in self.cards:
            if card.getRank() == 'A ' and value <= 11:
                value += 10
        return value

    def clear(self):
        self.cards = []

class Deck:
    def __init__(self, number_of_decks):
        self.playing_cards = []
        for _ in range(number_of_decks):
            for suit in SUITLIST:
                for rank in RANKLIST:
                    self.playing_cards.append(AsciiArtCard(suit, rank))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.playing_cards)

    def pop(self):
        return self.playing_cards.pop(0)
