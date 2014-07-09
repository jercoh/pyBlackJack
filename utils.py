# @author Jeremie Cohen - 090714
"""Various utility functions for handling prompt messages and console prints."""

def getInteger(message):
	"""Prompt message until the user types an integer"""
	while True:
		user_input = raw_input(message)
		try:
			return int(user_input)
		except ValueError:
			continue

def getIntegerInRange(message, min, max):
	"""Prompt message until the user types an integer in range(min, max)"""
	while True:
		user_input = getInteger(message)
		if user_input in range(min, max):
			return user_input

def multipleChoiceQuestion(message, choices):
	"""Prompt message until the user answers within one of the choices"""
	while True:
		user_input = raw_input(message).lower()
		if user_input in choices:
			return user_input
		continue

def getBoolean(message):
	"""Prompt message until the user answers with y or n"""
	user_input = multipleChoiceQuestion(message, ['y', 'n'])
	if user_input == 'y':
		return True
	return False

def printSeparator():
	print("=======================================================")
