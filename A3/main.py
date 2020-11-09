# Minimax Program to play connect 3
# Kevin Tayah
# CS380

import sys
import util
from agent import RandomPlayer, MinimaxPlayer
from human import HumanPlayer
from game import Game
import time

def main():
    player1 = None
    player2 = None
    player1Type = util.get_arg(1)
    player2Type = util.get_arg(2)

    if player1Type == None or player2Type == None:
        print('Invalid use of connect3 game')
        return

    if player1Type == 'human':
        player1 = HumanPlayer('X')
    elif player1Type == 'random':
        player1 = RandomPlayer('X')
    elif player1Type == 'minimax':
        player1 = MinimaxPlayer('X')
    
    if player2Type == 'human':
        player2 = HumanPlayer('O')
    elif player2Type == 'random':
        player2 = RandomPlayer('O')
    elif player2Type == 'minimax':
        player2 = MinimaxPlayer('O')        
    
    game = Game(player1, player2)
    winner = game.play()
    print('Winner:', winner)

if __name__ == "__main__":
	main()