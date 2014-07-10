# @author Jeremie Cohen - 070714
"""pyBlackJack main file"""
from cards import Deck
from players import Player, Dealer
import asciiArts
import utils

#####################################################

class BlackJack:
	"""Main class of pyBlackJack. Define a BlackJack game with a 6-deck shoe, one player and one dealer."""
	def __init__(self):
		# Create the deck
		self.deck = Deck(6)

		# Create the player
		self.player = Player(self.deck)

		# Create the dealer
		self.dealer = Dealer(self.deck, [self.player])

	def start(self):
		"""Starts the game. A game ends when the player has no more chips."""
		# Print game's title
		asciiArts.print_title()
		utils.print_separator()

		# While the player has enough money to play
		while self.player.get_bankroll() > 0:
			# Display player's bankroll
			print("Your current bankroll is: "+str(self.player.get_bankroll()))+" chips."

			# Play a game
			self.play()

			# End
			self.end()

		print("Thank you for playing pyBlackJack!")

	def play(self):
		"""Play a round. The player first bets and then play his hand(s)."""
		# Clear player's and dealer's hand
		self.player.clear()
		self.dealer.clear()

		# Ask for a bet
		bet = self.bet_step()

		# Register player's bet
		self.player.bet(bet)

		# If the dealer has dealt 75% of the cards, then shuffle a new deck
		if self.deck.get_number_of_cards_left() < 78:
			self.deck = Deck(6)

		# Deal cards
		print("Dealing...")
		self.dealer.deal()
		utils.print_separator()
		self.print_dealer_hand(False)

		# Check if hands can be split
		self.split_step()

		# Play player's hands
		for i in range(len(self.player.hands)):
			self.player.hand = self.player.hands[i]
			self.play_hand(i)

	def end(self):
		"""End of player's turn. The dealer plays and unveils his cards. The results are then displayed."""
		self.dealer.unveil_cards()
		self.dealer.hit_long()
		self.print_dealer_hand(True)
		self.display_results()

	def bet_step(self):
		"""The player choses how many chips he wants to bet."""
		while True:
			# Ask for the bet
			bet = utils.read_integer("Enter your bet (1 chip minimum): ")

			bankroll = self.player.get_bankroll()

			# If the bet is less than player's bankroll and higher than 1 chip, play the round
			if bet <= bankroll and bet >= 1:
				return bet

			# The bet is higher than player's bankroll
			elif bet >= bankroll:
				print("You cannot bet more than your current bankroll!")
				continue

			# The bet is lower than 1 chip
			elif bet < 1:
				print("The minimum bet is 1 chip!")
				continue

			# Other cases
			else:
				print("Wrong bet. Please enter a positive number greater than 1.")
				continue

	def split_step(self):
		"""If player's hand is a pair, he has to choose whether he wants to split it or not."""
		for i in range(len(self.player.hands)):
			# Check if player's hand is splittable (Player can play a maximum of 4 hands at the same time)
			if self.player.hand.is_splittable() and len(self.player.hands) < 4:

				# Print player's hand
				utils.print_separator()
				print("Player's hand #"+str(i)+":\n")
				self.print_player_hand()

				# Ask player whether he wants to split the hand or not
				do_split = utils.read_boolean("Do you want to split? (Y/N)")

				if do_split:
					# Check if player has enough chips to split
					if self.player.can_split():

						# Split the hand
						self.player.split()

						# Recursive call of split_bet to check if the new hands can also be split
						self.split_step()
						break

					else:
						print("Sorry, you don't have enough chips to split!")

	def play_hand(self, i):
		"""Play a hand."""
		# Print player's hand
		utils.print_separator()
		print("Player's hand #"+str(i)+":\n")
		self.print_player_hand()

		# Check if the hand is a BlackJack
		if self.player.hand.is_blackJack():
			self.player.hand.status = "blackjack"
			print("Congratulations! You got a Blackjack!\n")

		else:
			while self.player.hand.status == "active":
				# Ask for player's next move
				action = utils.multiple_choice_question("[H]it or [S]tand? (H/S): ", ['h', 's'])
				utils.print_separator()
				# If he stands
				if action == 's':
					# Finish the current hand
					self.player.hand.status = "finished"

				# If he hits
				elif action == 'h':
					# Hit
					self.player.hit()
					self.print_player_hand()

					# Check if player is busted
					if self.player.is_busted():
						self.player.hand.status = "busted"
						print("You bust!\n")

	def display_results(self):
		"""Compute player's gain and display results at the end of the round."""
		gain = 0

		# Check if dealer is busted
		if self.dealer.is_busted():
			print("Dealer is busted!\n")

			# Compute player's gain. Loop through player's hands
			for hand in self.player.hands:
				if hand.is_blackJack():
					gain += 2.5*self.player.get_bet()
				elif hand.status == "finished":
					gain += 2*self.player.get_bet()


		# Dealer got a BlackJack
		elif self.dealer.hand.is_blackJack():
			print("Dealer got a BlackJack!\n")

			# Compute player's gain. Loop through player's hands
			for hand in self.player.hands:
				if hand.is_blackJack():
					gain += self.player.get_bet()
		
		# Dealer has neither busted nor got a BlackJack
		else:
			# Compute player's gain. Loop through player's hands
			for hand in self.player.hands:
				if hand.is_blackJack():
					gain += 2.5*self.player.get_bet()
				elif hand.status == "finished":
					if hand.get_value() > self.dealer.hand.get_value():
						gain += 2*self.player.get_bet()
					elif hand.get_value() == self.dealer.hand.get_value():
						gain += self.player.get_bet()

		# Add gain to player's account
		self.player.bankroll += gain

		# Player wins chips
		if gain > 0:
			print("You won "+str(gain)+" chip(s)! Your new bankroll is: "+str(self.player.get_bankroll()))+" chips."

		# Player loses chips
		else:
			loss = len(self.player.hands)*self.player.get_bet()
			print("You lost "+str(loss)+" chip(s)... Your new bankroll is: "+str(self.player.get_bankroll()))+" chips."
		utils.print_separator()
		utils.print_separator()

	def print_dealer_hand(self, with_value):
		"""Print dealer's hand."""
		print("Dealer's hand:\n")
		if with_value:
			print("value: "+str(self.dealer.hand.get_value())+"\n"+str(self.dealer.hand))
		else:
			print(str(self.dealer.hand))

	def print_player_hand(self):
		"""Print player's current hand."""
		hand = self.player.hand
		print("value: "+str(hand.get_value())+"\n"+str(hand))

#####################################################

def main():
	"""Main function"""

	# Instantiate a BlackJack game
	game = BlackJack()@

	# Start the game
	game.start()

if __name__ == '__main__':
    main()
