from cards import Deck
from players import Player, Dealer
import asciiArts
import utils

#####################################################

class BlackJack:
	def __init__(self):
		self.deck = Deck(6)
		self.player = Player(self.deck)
		self.dealer = Dealer(self.deck, [self.player])
		self.in_round = True

	def start(self):
		asciiArts.printTitle()
		print("Your balance is: $"+str(self.player.getBalance()))
		self.betStep()

	def betStep(self):
		while self.player.getBalance() > 0:
			self.player.clear()
			self.dealer.clear()
			utils.printSeparator()
			bet = utils.getInteger("Enter your bet ($1 minimum): ")
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
		# Player has won or lose
		if self.gameIsOver():
			self.dealer.unveilCards()
			utils.printSeparator()
			self.printHands()
			print(self.end_message)

		# Player has to make a move
		else:
			self.printHands()
			action = utils.multipleChoiceQuestion("[H]it or [S]tand?: ", ['h', 's'])
			if action == 's':
				self.dealer.hitLong()
				self.in_round = False
			elif action == 'h':
				self.player.hit()
			self.playRound()


	def gameIsOver(self):
		# Player has a BlackJack
		if self.player.blackJack():
			# Dealer has also a BlackJack
			if self.dealer.blackJack():
				self.player.balance += self.player.getBet()
				self.end_message = "Even! Your new balance is: $"+str(self.player.getBalance())
			else:
				self.player.balance += 2.5*self.player.getBet()
				self.end_message = "BlackJack! Your new balance is: $"+str(self.player.getBalance())
			return True

		# Player wins the round
		elif self.playerWins():
			self.player.balance += 2*self.player.getBet()
			self.end_message = "You win! Your new balance is: $"+str(self.player.getBalance())
			return True

		# Player loses the round
		elif self.playerLoses():
			self.end_message = "You Lose :( ! Your new balance is: $"+str(self.player.getBalance())
			return True

		# Player's hand has the same value as Dealer's
		elif self.even():
			self.player.balance += self.player.getBet()
			self.end_message = "Even! Your new balance is: $"+str(self.player.getBalance())
			return True
		else:
			return False

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
		print("Player: (value: "+str(self.player.hand.getValue())+")\n"+str(self.player.hand))
		print("Dealer:\n"+str(self.dealer.hand))

#####################################################

def main():
    game = BlackJack()
    game.start()

if __name__ == '__main__':
    main()