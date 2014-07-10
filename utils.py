# @author Jeremie Cohen - 090714
"""Various utility functions for handling prompt messages and console prints."""

def read_integer(message):
	"""Prompt message until the user types an integer"""
	while True:
		user_input = raw_input(message)
		try:
			return int(user_input)
		except ValueError:
			continue

def read_integer_in_range(message, min, max):
	"""Prompt message until the user types an integer in range(min, max)"""
	while True:
		user_input = read_integer(message)
		if user_input in range(min, max):
			return user_input

def multiple_choice_question(message, choices):
	"""Prompt message until the user answers within one of the choices"""
	while True:
		user_input = raw_input(message).lower()
		if user_input in choices:
			return user_input
		continue

def read_boolean(message):
	"""Prompt message until the user answers with y or n"""
	user_input = multiple_choice_question(message, ['y', 'n'])
	if user_input == 'y':
		return True
	return False

def print_separator():
	print("=======================================================")
