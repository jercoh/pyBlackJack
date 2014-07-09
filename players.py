from cards import Hand

#####################################################

class User:
    def __init__(self, deck):
        self.hand = Hand()
        self.deck = deck

    def hit(self):
        self.hand.deal(self.deck.pop())

    def bust(self):
        return self.hand.get_value() > 21

    def blackJack(self):
        return len(self.hand.cards) == 2 and self.hand.get_value() == 21

    def clear(self):
        self.hand.clear()

#####################################################

class Player(User):
    def __init__(self, deck):
        User.__init__(self, deck)
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

#####################################################

class Dealer(User):
    def __init__(self, deck, players):
        User.__init__(self, deck)
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


