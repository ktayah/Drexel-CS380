# Agent Program to solve a rgb problem
# Kevin Tayah
# CS380

import sys
import rgb
import util
from agent import Agent

DEFAULT_N = 8

def main():
    command = util.get_arg(1)
    state = rgb.State(util.get_arg(2))
    agent = Agent()

    if command == 'random':
        agent.random_walk(state, DEFAULT_N)
    elif command == 'bfs':
        agent.bfs(state)
    elif command == 'dfs':
        agent.dfs(state)
    elif command == 'a_star':
        agent.a_star(state)
    else:
        print('Invalid command inputed')

if __name__ == "__main__":
	main()