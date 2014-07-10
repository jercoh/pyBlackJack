# @author Jeremie Cohen - 070714
from cards import Hand

#####################################################

class User:
    def __init__(self, deck):
        self.deck = deck

    def hit(self):
        self.hand.deal(self.deck.pop())

    def is_busted(self):
        return self.hand.get_value() > 21

#####################################################

class Player(User):
    def __init__(self, deck):
        User.__init__(self, deck)
        self.hands = [Hand()]
        self.hand = self.hands[0]
        self.balance = 100
        self.starting_bet = 0

    def bet(self, bet):
        if bet >= 1:
            self.starting_bet = bet
            self.balance -= bet

    def get_bet(self):
        return self.starting_bet

    def get_balance(self):
        return self.balance

    def split(self):
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

    def can_split(self):
        return self.balance >= self.starting_bet

    def clear(self):
        self.hands = [Hand()]
        self.hand = self.hands[0]


#####################################################

class Dealer(User):
    def __init__(self, deck, players):
        User.__init__(self, deck)
        self.hand = Hand()
        self.players = players

    def deal(self):
        for _ in range(2):
            for player in self.players:
                player.hit()
            self.hit()
        self.hand.cards[0].face_down()
    
    def hit_long(self):
        while self.hand.get_value() < 17:
            self.hit()

    def unveil_cards(self):
        self.hand.cards[0].face_up()

    def clear(self):
        self.hand.clear()


