# Rotator Program to solve a rotator problem
# Kevin Tayah
# CS380
import sys
import copy

DEFAULT_STATE = '12345|1234 |12354'

class State:
	state = []

	def __init__(self, stateString):
		splitStateString = stateString.split('|')
		for rowString in splitStateString:
			self.state.append(list(rowString))

	def __str__(self):
		self.print()
	
	def __eq__(self, other):
		return self.state == other.state

	def execute(self, action):
		newState = action.execute()
		if newState != None:
			self.state = newState.copy()
			return self
	
	def print(self):
		printString = ''
		for row in self.state:
			for col in row:
				printString += col
			printString += '|'
		
		printString = printString[:-1]
		print(printString)

	def is_goal(self):
		transposed = [[None for j in range(len(self.state))] for i in range(len(self.state[0]))]
		
		for i, row in enumerate(self.state):
			for j, value in enumerate(row):
				transposed[j][i] = value

		for row in transposed:
			element = row[0] if row[0] != ' ' else row[1] # Grab the element that is not a space
			for col in row:
				if col != element and col != ' ':
					return False
		
		return True

	def clone(self):
		return copy.deepcopy(self.state)
	
	def actions(self):
		possibleRotateActions = []
		possibleSlideActions = []
		stateLength = len(self.state)
		for rowIndex in range(stateLength):
			rowLength = len(self.state[rowIndex])
			possibleRotateActions.append(Action(self.clone(), 'rotate({},{})'.format(rowIndex, -1)))
			possibleRotateActions.append(Action(self.clone(), 'rotate({},{})'.format(rowIndex, 1)))
			for colIndex in range(rowLength):
				if self.state[rowIndex][colIndex] == ' ':
					if rowIndex - 1 >= 0:
						possibleSlideActions.append(Action(self.clone(), 'slide({},{},{},{})'.format(colIndex, rowIndex - 1, colIndex, rowIndex)))
					if rowIndex + 1 < rowLength:
						possibleSlideActions.append(Action(self.clone(), 'slide({},{},{},{})'.format(colIndex, rowIndex + 1, colIndex, rowIndex)))

					if colIndex == (rowLength - 1):
						possibleSlideActions.append(Action(self.clone(), 'slide({},{},{},{})'.format(0, rowIndex, colIndex, rowIndex)))
						possibleSlideActions.append(Action(self.clone(), 'slide({},{},{},{})'.format(colIndex - 1, rowIndex, colIndex, rowIndex)))
					elif colIndex == 0:
						possibleSlideActions.append(Action(self.clone(), 'slide({},{},{},{})'.format(rowLength - 1, rowIndex, colIndex, rowIndex)))
						possibleSlideActions.append(Action(self.clone(), 'slide({},{},{},{})'.format(colIndex + 1, rowIndex, colIndex, rowIndex)))
					else:
						possibleSlideActions.append(Action(self.clone(), 'slide({},{},{},{})'.format(colIndex - 1, rowIndex, colIndex, rowIndex)))
						possibleSlideActions.append(Action(self.clone(), 'slide({},{},{},{})'.format(colIndex + 1, rowIndex, colIndex, rowIndex)))
		return possibleRotateActions + possibleSlideActions
	
	def walk(self, n):
		keepWalking = True
		statesSeen = [self.state]
		if n > len(self.actions()):
			print("action[{}] does not exist, try a lower walk value".format(n))
			return

		while keepWalking:
			self.print()
			possibleActions = self.actions()

			if len(possibleActions) == 0 or n >= len(possibleActions):
				print("action[{}] does not exist, try a lower walk value".format(n))
				return

			self.execute(possibleActions[n])
			if self.state in statesSeen:
				keepWalking = False
			else:
				statesSeen.append(self.state)

class Action:
	state = None
	action = ''

	def __init__(self, state, action):
		self.state = state
		self.action = action
	
	def __str__(self):
		return self.action
	
	def __eq__(self, value):
		return value.state == self.state

	def slide(self, x, y, x2, y2):
		tileToMove = self.state[y][x]
		emptyTile = self.state[y2][x2]
		if emptyTile == ' ':
			self.state[y][x] = emptyTile
			self.state[y2][x2] = tileToMove
			return self.state
		else:
			print('Invalid Usage of Slide')
			return None

	def rotate(self, y, dx):
		if dx == -1 and y < len(self.state):
			modifiedRow = self.state[y][1:]
			modifiedRow.append(self.state[y][0])
			self.state[y] = modifiedRow
			return self.state
		elif dx == 1 and y < len(self.state):
			lastItem = self.state[y].pop()
			self.state[y].insert(0, lastItem)
			return self.state
		else:
			print('Invalid Usage of Rotate')
			return None
	
	def execute(self):
		[actionType, parameters] = self.action.split('(')
		if actionType == 'rotate':
			y, dx = parameters[:-1].split(',')
			return self.rotate(int(y), int(dx))
		elif actionType == 'slide':
			x, y, x2, y2 = parameters[:-1].split(',')
			return self.slide(int(x), int(y), int(x2), int(y2))
		else:
			print('Invalid usage of execute')

def main():
	command = sys.argv[1] # This is the command to run
	stateString = None # This the optional argument

	if len(sys.argv) == 3:
		stateString = sys.argv[2]
	else:
		stateString = DEFAULT_STATE

	rotator = State(stateString)

	if command == 'print':
		rotator.print()
	elif command == 'goal':
		print(rotator.is_goal())
	elif command == 'actions':
		for possibleAction in rotator.actions():
			print(possibleAction)
	elif "walk" in command:
		n = int(command[4:])
		rotator.walk(n)
	else:
		print('Invalid usage of program')

if __name__ == "__main__":
	main()
