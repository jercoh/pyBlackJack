from cards import Deck
from players import Player, Dealer

class BlackJack:
	def __init__(self):
		self.deck = Deck(6)
		self.player = Player(self.deck)
		self.dealer = Dealer(self.deck, [self.player])
		self.in_round = True

	def start(self):
		print "Welcome to pyBlackJack!\n"
		print("Your balance is: "+str(self.player.getBalance()))
		self.betStep()

	def betStep(self):
		while self.player.getBalance() > 0:
			self.player.clear()
			self.dealer.clear()
			bet_input = raw_input("Enter your bet ($1 minimum): ") 
			bet = int(bet_input)
			balance = self.player.getBalance()
			if bet <= balance and bet >= 1:
				self.player.bet(bet)
				print("Dealing...")
				self.dealer.deal()
				self.in_round = True
				self.playRound()
			elif bet >= balance:
				print("You cannot bet more than your current balance!")
				continue
			elif bet < 1:
				print("The minimum bet is $1!")
				continue
			else:
				print("Wrong bet. Please enter a positive number greater than 1.")
				continue

	def playRound(self):
		self.printHands()
		# Player has a BlackJack
		if self.player.blackJack():
			# Dealer has also a BlackJack
			if self.dealer.blackJack():
				self.player.balance += self.player.getBet()
				print("Even! Your new balance is: "+str(self.player.getBalance()))
			else:
				self.player.balance += 2.5*self.player.getBet()
				print("BlackJack! Your new balance is: "+str(self.player.getBalance()))
			return
		# Player wins the round
		elif self.playerWins():
			self.player.balance += 2*self.player.getBet()
			print("You win! Your new balance is: "+str(self.player.getBalance()))
			return
		# Player loses the round
		elif self.playerLoses():
			print("You Lose :( ! Your new balance is: "+str(self.player.getBalance()))
			return
		# Player hand has the same value as Dealer's
		elif self.even():
			self.player.balance += self.player.getBet()
			print("Even! Your new balance is: "+str(self.player.getBalance()))
			return
		# Player has to make a move
		else:
			action = raw_input("Hit or Stand?(h/s): ")
			if action == 's':
				self.dealer.hitLong()
				self.in_round = False
			elif action == 'h':
				self.player.hit()
			else:
				print("Wrong input. What is your next move?\n")
			self.playRound()


	def playerWins(self):
		dealerValue = self.dealer.hand.getValue()
		playerValue = self.player.hand.getValue()
		return self.in_round == False and ((self.dealer.bust() and playerValue <= 21) or (dealerValue < playerValue))

	def playerLoses(self):
		dealerValue = self.dealer.hand.getValue()
		playerValue = self.player.hand.getValue()
		return (self.in_round == False and (dealerValue > playerValue)) or self.player.bust()

	def even(self):
		dealerValue = self.dealer.hand.getValue()
		playerValue = self.player.hand.getValue()
		return self.in_round == False and (dealerValue == playerValue)

	def printHands(self):
		print("Player:"+str(self.player.hand.getValue())+"\n"+str(self.player.hand))
		print("Dealer:\n"+str(self.dealer.hand))

def main():
    game = BlackJack()
    game.start()


if __name__ == '__main__':
    main()