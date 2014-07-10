# @author Jeremie Cohen - 070714
"""Cards, hand and deck models. A hand contains 2 or more cards. A deck contains a multiple of 52 cards."""
import random

SUITLIST = ('heart', 'diamond', 'spade', 'club')
RANKLIST = ('A ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ',
            '8 ', '9 ', '10', 'J ', 'Q ', 'K ')
VALUEMAP = {'A ':1, '2 ':2, '3 ':3, '4 ':4, '5 ':5,
            '6 ':6, '7 ':7, '8 ':8, '9 ':9, '10':10,
            'J ':10, 'Q ':10, 'K ':10}
TOP = " _______"
BOTTOM = "|_____"

#####################################################

class Card:
    """Define a card"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

    def get_suit(self):
        """Return card's suit"""
        return self.suit

    def get_rank(self):
        """Return card's rank"""
        return self.rank

    def get_value(self):
        """Return card's blackjack value"""
        return VALUEMAP[self.rank]

    def valid_suits():
        """Return the list of valid suits"""
        return SUITLIST

#####################################################

class AsciiArtCard(Card):
    """Define a AsciiArt card. Inherits from Card."""
    def __init__(self, rank, suit):
        Card.__init__(self, rank, suit)
        self.top_line = TOP
        self.face_up()

    def face_up(self):
        """Flip an AsciiArt card face up."""
        if self.get_suit() == "spade":
            self.first_line = "|"+self.get_rank()+" .   |"
            self.second_line = "|  /.\  |"
            self.third_line = "| (_._) |"
            self.fourth_line = "|   |   |"
        elif self.get_suit() == "club":
            self.first_line = "|"+self.get_rank()+" _   |"
            self.second_line = "|  ( )  |"
            self.third_line = "| (_'_) |"
            self.fourth_line = "|   |   |"
        elif self.get_suit() == "heart":
            self.first_line = "|"+self.get_rank()+"_ _  |"
            self.second_line = "| ( v ) |"
            self.third_line = "|  \ /  |"
            self.fourth_line = "|   .   |"
        elif self.get_suit() == "diamond":
            self.first_line = "|"+self.get_rank()+" .   |"
            self.second_line = "|  / \  |"
            self.third_line = "|  \ /  |"
            self.fourth_line = "|   v   |"
        self.bottom_line = BOTTOM+self.get_rank()+"|"

    def face_down(self):
        """Flip an AsciiArt card face down."""
        self.first_line = "| * * * |"
        self.second_line = "| * * * |"
        self.third_line = "| * * * |"
        self.fourth_line = "| * * * |"
        self.bottom_line = BOTTOM+"__|"

#####################################################

class Hand:
    """Define a Hand of Cards. Its status is either 'active', 'busted', blackjack' or 'finished'."""
    def __init__(self):
        self.cards = []
        self.status = "active"

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

    def get_value(self):
        """Return hand's total value"""
        value = 0
        contains_an_ace = False
        for card in self.cards:
            value += card.get_value()
            if card.get_rank() == 'A ':
                contains_an_ace = True
        if contains_an_ace and value <= 11:
            value += 10
        return value

    def deal(self, card):
        """Add a card to the hand"""
        self.cards.append(card)

    def clear(self):
        """Remove all cards from the hand"""
        self.cards = []

    def is_blackJack(self):
        """Return True if the hand is a BlackJack"""
        return len(self.cards) == 2 and self.get_value() == 21

    def is_splittable(self):
        """Return True if the hand is a splittable pair"""
        if len(self.cards) == 2 and len(set([self.cards[0].get_rank(), self.cards[1].get_rank()])) == 1:
            return True
        return False

#####################################################

class Deck:
    """Define a deck of cards."""
    def __init__(self, number_of_decks):
        self.playing_cards = []
        for _ in range(number_of_decks):
            for suit in SUITLIST:
                for rank in RANKLIST:
                    self.playing_cards.append(AsciiArtCard(suit, rank))
        self.shuffle()

    def shuffle(self):
        """Randomly shuffle the deck"""
        random.shuffle(self.playing_cards)

    def pop(self):
        """Pop a card from the top of the deck"""
        return self.playing_cards.pop(0

    def get_number_of_cards_left(self):
        """Return the number of cards remaining in the deck"""
        return len(self.playing_cards))
