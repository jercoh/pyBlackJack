# @author Jeremie Cohen - 090714
"""Various utility functions for handling prompt messages and user input."""

def getInteger(message):
	"""Prompt message until the user types an integer"""
	while True:
		user_input = raw_input(message)
		try:
			return int(user_input)
		except ValueError:
			continue

def multipleChoiceQuestion(message, choices):
	"""Prompt message until the user answers with one of the choices"""
	while True:
		user_input = raw_input(message).lower()
		if user_input in choices:
			return user_input
		continue

def getBoolean(message):
	"""Prompt message until the user answers with y or n"""
	user_input = askForChoice(message, ['y', 'n'])
	if user_input == 'y':
		return True
	return False
