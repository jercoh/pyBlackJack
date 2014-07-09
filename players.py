from cards import Hand

#####################################################

class User:
    def __init__(self, deck):
        self.hand = Hand()
        self.deck = deck

    def hit(self):
        self.hand.deal(self.deck.pop())

    def bust(self):
        return self.hand.getValue() > 21

    def blackJack(self):
        return len(self.hand.cards) == 2 and self.hand.getValue() == 21

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

    def getBet(self):
        return self.starting_bet

    def getBalance(self):
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
        self.hand.cards[0].faceDown()
    
    def hitLong(self):
        while self.hand.getValue() < 17:
            self.hit()

    def unveilCards(self):
        self.hand.cards[0].faceUp()


