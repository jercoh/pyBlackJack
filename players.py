# @author Jeremie Cohen - 070714
"""User model. PLayer and Dealer class inherits from User."""
from cards import Hand

#####################################################

class User:
    """Define a User"""
    def __init__(self, deck):
        self.deck = deck

    def hit(self):
        """The user takes a hit. Add a card to user's hand."""
        self.hand.deal(self.deck.pop())

    def is_busted(self):
        """Return True if user hand's value exceeds 21."""
        return self.hand.get_value() > 21

#####################################################

class Player(User):
    """Define a player that can have several hands (4 max.). A player starts with 100 chips and can bet at least 1 chip."""
    def __init__(self, deck):
        User.__init__(self, deck)
        self.hands = [Hand()]
        self.hand = self.hands[0]
        self.bankroll = 100
        self.starting_bet = 0

    def get_bet(self):
        """Return player's bet."""
        return self.starting_bet

    def get_bankroll(self):
        """Return player's bankroll."""
        return self.bankroll

    def can_split(self):
        """Check if the player has enough chips to split."""
        return self.bankroll >= self.starting_bet

    def bet(self, bet):
        """Define how many chips, the player is betting."""
        if bet >= 1:
            self.starting_bet = bet
            self.bankroll -= bet

    def split(self):
        """Split a hand containing a pair. Create two separate hands that have the same first card."""
        # Create a new hand
        new_hand = Hand()

        # Add current hand's first card to the new hand
        new_hand.deal(self.hand.cards[0])

        # Remove the first card from the splitted hand
        self.hand.cards.pop(0)

        # Complete both hands with a card
        new_hand.deal(self.deck.pop())
        self.hand.deal(self.deck.pop())

        # Add the new hand to self.hands array
        self.hands.append(new_hand)

    def clear(self):
        """Remove player's hands."""
        self.hands = [Hand()]
        self.hand = self.hands[0]


#####################################################

class Dealer(User):
    """Define the dealer."""
    def __init__(self, deck, players):
        User.__init__(self, deck)
        self.hand = Hand()
        self.players = players

    def deal(self):
        """The dealer deals two cards to the player. Dealer's first card is face down."""
        for _ in range(2):
            for player in self.players:
                player.hit()
            self.hit()
        self.hand.cards[0].face_down()
    
    def hit_long(self):
        """The dealer hits until 17. In pyBlackJack dealer stands on soft 17."""
        while self.hand.get_value() < 17:
            self.hit()

    def unveil_cards(self):
        """Unveil dealer's cards."""
        self.hand.cards[0].face_up()

    def clear(self):
        """Remove dealer's hand."""
        self.hand.clear()
