# @author Jeremie Cohen - 070714
from cards import Deck
from players import Player, Dealer
import asciiArts
import utils

#####################################################

class BlackJack:
	def __init__(self):
		# Create the deck
		self.deck = Deck(6)

		# Create the player
		self.player = Player(self.deck)

		# Create the dealer
		self.dealer = Dealer(self.deck, [self.player])

		# Start a new round
		self.in_round = True

	def start(self):
		# Print game title
		asciiArts.print_title()

		# While the player has enough money to play
		while self.player.get_balance() > 0:
			# Display player's balance
			print("Your current balance is: $"+str(self.player.get_balance()))

			# Play a game
			self.play()

			# End
			self.end()

		print("Thank you for playing pyBlackJack!")

	def play(self):
		# Clear player's and dealer's hand
		self.player.clear()
		self.dealer.clear()

		utils.print_separator()

		#Ask for bet
		bet = self.bet_step()

		# Update player's balance
		self.player.bet(bet)

		# If the dealer dealt 75% of the cards, shuffle a new deck
		if self.deck.get_number_of_cards_left() < 78:
			self.deck = Deck(6)

		# Deal cards
		print("Dealing...")
		self.dealer.deal()
		self.print_dealer_hand()
		# print("Player's hand:\n")
		# self.print_player_hand()

		# Start the round
		self.in_round = True

		# Check if hands can be split
		self.split_step()

		# Play player's hands
		for i in range(len(self.player.hands)):
			self.player.hand = self.player.hands[i]
			self.play_hand(i)

	def end(self):
		self.dealer.unveil_cards()
		self.dealer.hit_long()
		self.print_dealer_hand()
		self.display_results()

	def bet_step(self):
		while True:
			# Ask for the bet
			bet = utils.get_integer("Enter your bet ($1 minimum): ")

			balance = self.player.get_balance()

			# If the bet is less than player's balance and higher than $1, play the round
			if bet <= balance and bet >= 1:
				return bet

			# The bet is higher than player's balance
			elif bet >= balance:
				print("You cannot bet more than your current balance!")
				continue

			# The bet is lower than $1
			elif bet < 1:
				print("The minimum bet is $1!")
				continue

			# Other cases
			else:
				print("Wrong bet. Please enter a positive number greater than 1.")
				continue

	def split_step(self):
		for i in range(len(self.player.hands)):
			# Check if the hand is splittable (Player can play a maximum of 4 hands at the same time)
			if self.player.hand.is_splittable() and len(self.player.hands) < 4:
				print("Player's hand #"+str(i)+":\n")
				self.print_player_hand()
				do_split = utils.get_boolean("Do you want to split? (Y/N)")
				if do_split:
					if self.player.can_split():
						self.player.split()
						#self.print_splitted_hands()

						# Check if the new hands can also be splitted
						self.split_step()
						break
					else:
						print("Sorry, you don't have enough money to split!")

	def play_hand(self, i):
		print("Player's hand #"+str(i)+":\n")
		self.print_player_hand()
		if self.player.hand.is_blackJack():
			self.player.hand.status = "blackjack"
			print("Congratulations! You got a Blackjack!\n")
		else:
			while self.player.hand.status == "active":
				action = utils.multiple_choice_question("[H]it or [S]tand? (H/S): ", ['h', 's'])
				if action == 's':
					self.player.hand.status = "finished"
				elif action == 'h':
					self.player.hit()
					self.print_player_hand()
					if self.player.is_busted():
						self.player.hand.status = "busted"
						print("You bust!\n")

	def display_results(self):
		gain = 0
		if self.dealer.is_busted():
			print("Dealer is busted!\n")
			for hand in self.player.hands:
				if hand.is_blackJack():
					gain += 2.5*self.player.get_bet()
				elif hand.status == "finished":
					gain += 2*self.player.get_bet()

		elif self.dealer.hand.is_blackJack():
			print("Dealer got a BlackJack!\n")
			for hand in self.player.hands:
				if hand.is_blackJack():
					gain += self.player.get_bet()
		
		else:
			for hand in self.player.hands:
				if hand.is_blackJack():
					gain += 2.5*self.player.get_bet()
				elif hand.status == "finished":
					if hand.get_value() > self.dealer.hand.get_value():
						gain += 2*self.player.get_bet()
					elif hand.get_value() == self.dealer.hand.get_value():
						gain += self.player.get_bet()

		self.player.balance += gain

		if gain > 0:
			print("You won $"+str(gain)+"! Your new balance is: $"+str(self.player.get_balance()))
		else:
			loss = len(self.player.hands)*self.player.get_bet()
			print("You lost $"+str(loss)+"... Your new balance is: $"+str(self.player.get_balance()))

	def print_dealer_hand(self):
		utils.print_separator()
		print("Dealer's hand:\n"+str(self.dealer.hand))

	def print_player_hand(self):
		hand = self.player.hand
		utils.print_separator()
		print("value: "+str(hand.get_value())+"\n"+str(hand))

#####################################################

def main():
	game = BlackJack()
	game.start()

if __name__ == '__main__':
    main()