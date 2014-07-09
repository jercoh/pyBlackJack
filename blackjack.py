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
		asciiArts.print_title()
		print("Your balance is: $"+str(self.player.get_balance()))
		self.bet_step()

	def bet_step(self):
		while self.player.get_balance() > 0:
			self.player.clear()
			self.dealer.clear()
			utils.print_separator()
			bet = utils.get_integer("Enter your bet ($1 minimum): ")
			balance = self.player.get_balance()
			if bet <= balance and bet >= 1:
				self.player.bet(bet)
				# The dealer deals 75% of the cards before a new shuffle
				if self.deck.get_number_of_cards_left() < 78:
					self.deck = Deck(6)
				print("Dealing...")
				self.dealer.deal()
				self.in_round = True
				self.round()
			elif bet >= balance:
				print("You cannot bet more than your current balance!")
				continue
			elif bet < 1:
				print("The minimum bet is $1!")
				continue
			else:
				print("Wrong bet. Please enter a positive number greater than 1.")
				continue

	def round(self):
		# Player has won or lose
		if self.is_game_over():
			self.dealer.unveil_cards()
			utils.print_separator()
			self.print_hands()
			print(self.end_message)

		# Player has to make a move
		else:
			self.print_hands()
			action = utils.multiple_choice_question("[H]it or [S]tand?: ", ['h', 's'])
			if action == 's':
				self.dealer.hit_long()
				self.in_round = False
			elif action == 'h':
				self.player.hit()
			self.round()


	def is_game_over(self):
		# Player has a BlackJack
		if self.player.blackJack():
			# Dealer has also a BlackJack
			if self.dealer.blackJack():
				self.player.balance += self.player.get_bet()
				self.end_message = "Even! Your new balance is: $"+str(self.player.get_balance())
			else:
				self.player.balance += 2.5*self.player.get_bet()
				self.end_message = "BlackJack! Your new balance is: $"+str(self.player.get_balance())
			return True

		# Player wins the round
		elif self.player_wins():
			self.player.balance += 2*self.player.get_bet()
			self.end_message = "You win! Your new balance is: $"+str(self.player.get_balance())
			return True

		# Player loses the round
		elif self.player_loses():
			self.end_message = "You Lose :( ! Your new balance is: $"+str(self.player.get_balance())
			return True

		# Player's hand has the same value as Dealer's
		elif self.even():
			self.player.balance += self.player.get_bet()
			self.end_message = "Even! Your new balance is: $"+str(self.player.get_balance())
			return True
		else:
			return False

	def player_wins(self):
		dealer_value = self.dealer.hand.get_value()
		player_value = self.player.hand.get_value()
		return self.in_round == False and ((self.dealer.bust() and player_value <= 21) or (dealer_value < player_value))

	def player_loses(self):
		dealer_value = self.dealer.hand.get_value()
		player_value = self.player.hand.get_value()
		return (self.in_round == False and (dealer_value > player_value)) or self.player.bust()

	def even(self):
		dealer_value = self.dealer.hand.get_value()
		player_value = self.player.hand.get_value()
		return self.in_round == False and (dealer_value == player_value)

	def print_hands(self):
		print("Player: (value: "+str(self.player.hand.get_value())+")\n"+str(self.player.hand))
		print("Dealer:\n"+str(self.dealer.hand))

#####################################################

def main():
	game = BlackJack()
	game.start()

if __name__ == '__main__':
    main()