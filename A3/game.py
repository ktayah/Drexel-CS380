from abc import ABC, abstractmethod
from connect3 import State
import util

class Player(ABC):
    token = None

    def __init__(self, token):
        self.token = token
        super().__init__()

    @abstractmethod
    def choose_action(self, state):
        pass

class Game:
    gameState = None
    player1 = None
    player2 = None

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play(self):
        self.gameState = State()

        while not self.gameState.game_over():
            player1Action = self.player1.choose_action(self.gameState)
            self.gameState.execute(player1Action)
            util.pprint(self.gameState)
            
            if self.gameState.game_over():
                break
            
            player2Action = self.player2.choose_action(self.gameState)
            self.gameState.execute(player2Action)
            util.pprint(self.gameState)
    
        return self.gameState.winner()