import random
import math
from game import Player
from connect3 import State

ROW_COUNT = 3
COLUMN_COUNT = 4

class RandomPlayer(Player):
    def choose_action(self, state):
        actionIndex = random.randint(0, len(state.actions(self.token)) - 1)
        return state.actions(self.token)[actionIndex]

class MinimaxPlayer(Player):
    bestAction = None

    def checkTwos(self, state, token, disjoint = False):
        numOfTwos = 0
        c = 2 if disjoint else 1
        for y, row in enumerate(state.board):
            for x, element in enumerate(row):
                if element == token:
                    if state.get(x, y + c) == token and y == ROW_COUNT - 2: # Vertical
                        if not disjoint:
                            numOfTwos += 1
                    if state.get(x + c, y) == token: # Horizontal
                        if not disjoint or (disjoint and state.get(x + c - 1, y) == ' '):
                            numOfTwos += 1
                    if y == 0 and state.get(x + c, y + c) == token: # Top-Bottom diagonal
                        if not disjoint or (disjoint and state.get(x + c - 1, y + c - 1) == ' '):
                            numOfTwos += 1
                    if y == ROW_COUNT - 1 and state.get(x - c, y + c) == token: # Bottom-Top diagonal
                        if not disjoint or (disjoint and state.get(x - c + 1, y + c - 1) == ' '):
                            numOfTwos += 1
        return numOfTwos

    def isWinningMovePossible(self, state, token):
        # Originally this function returned math.inf or -math.inf but I found it avoiding certain moves that could led to a win
        winningMoves = 0
        for y, row in enumerate(state.board):
            for x, element in enumerate(row):
                if element == token:
                    # Vertical Check
                    if state.get(x, y + 1) == token and state.get(x, y - 1) == ' ':
                        winningMoves += 1
                    # Horizontal Check
                    if (state.get(x + 1, y) == token or state.get(x - 1, y) == token) and (state.get(x + 1, y) == ' ' or state.get(x - 1, y) == ' '):
                        winningMoves += 1
                    # Top-Bottom diagonal
                    if (state.get(x + 1, y + 1) == token or state.get(x - 1, y - 1) == token) and (state.get(x + 1, y + 1) == ' ' or state.get(x - 1, y - 1) == ' ') and (state.get(x - 1, y) != ' ' or state.get(x + 1, y) != ' '):
                        winningMoves += 1
                    # Bottom-Top diagonal
                    if (state.get(x - 1, y + 1) == token or state.get(x + 1, y - 1) == token) and (state.get(x - 1, y + 1) == ' ' or state.get(x + 1, y - 1) == ' ') and (state.get(x - 1, y) != ' ' or state.get(x + 1, y) != ' '):
                        winningMoves += 1
                elif element == ' ':
                    # Vertical Check
                    if state.get(x, y + 1) == token and state.get(x, y + 2) == token:
                        winningMoves += 1
                    # Horizontal Check
                    if state.get(x + 1, y) == token and state.get(x - 1, y) == token and state.get(x, y + 1) != ' ':
                        winningMoves += 1
                    # Top-Bottom diagonal
                    if state.get(x + 1, y + 1) == token and state.get(x - 1, y - 1) == token and state.get(x, y + 1) != ' ':
                        winningMoves += 1
                    # Bottom-Top diagonal
                    if state.get(x - 1, y + 1) == token and state.get(x + 1, y - 1) == token and state.get(x, y + 1) != ' ':
                        winningMoves += 1
        return winningMoves

    def heuristic(self, state, depth, token):
        opponentToken = 'O' if token == 'X' else 'X'
        win = 1
        loss = 1

        # Handle if the current state is winning or losing
        if state.winner() == token:
            win = 1000
        elif state.winner() == opponentToken:
            loss = -1000

        winningMoves = self.isWinningMovePossible(state, token) * 100
        oppWinningMoves = self.isWinningMovePossible(state, opponentToken) * 100
        twos = self.checkTwos(state, token) # Number of connected tokens
        disjointedTwos = self.checkTwos(state, token, True) # Number of tokens that could be connected to a winning state next
        oppTwos = self.checkTwos(state, opponentToken)
        oppDisjointedTwos = self.checkTwos(state, opponentToken, True)

        return depth * win * loss * ((twos + disjointedTwos + winningMoves) - (oppTwos + oppDisjointedTwos + oppWinningMoves))

    def minimax(self, state, depth, maximizingPlayer):
        token = self.token if maximizingPlayer else self.opponentToken
        
        if state.game_over():
            return self.heuristic(state, depth, token)

        if maximizingPlayer:
            maxEval = -math.inf
            for action in state.actions(token):
                newState = state.clone().execute(action)
                eval = self.minimax(newState, depth + 1, False)
                if eval > maxEval:
                    self.bestAction = action
                    maxEval = eval
            return maxEval

        else:
            minEval = math.inf
            for action in state.actions(token):
                newState = state.clone().execute(action)
                eval = self.minimax(newState, depth + 1, True)
                minEval = min(minEval, eval)
            return minEval
    

    def choose_action(self, state):
        self.opponentToken = 'O' if self.token == 'X' else 'X'
        score = self.minimax(state, 0, True)
        
        return self.bestAction
