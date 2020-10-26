# Agent Program to solve a rgb problem
# Kevin Tayah
# CS380

import sys
import rgb
import util
from agent import Agent
import time

DEFAULT_N = 8

def heuristic(state, depth):
    h = 0

    stateStringValue = str(state)
    for elementIndex, element in enumerate(stateStringValue):
        if element == '|' or element == ' ': continue
        if elementIndex + 1 < len(stateStringValue) and element == stateStringValue[elementIndex + 1]:
            h += 1
        if elementIndex - 1 >= 0 and element == stateStringValue[elementIndex - 1]:
            h += 1
        if elementIndex + 5 < len(stateStringValue) and element == stateStringValue[elementIndex + 5]:
            h += 1
        if elementIndex - 5 >= 0 and element == stateStringValue[elementIndex - 5]:
            h += 1
    return h + depth

def main():
    command = util.get_arg(1)
    state = rgb.State(util.get_arg(2))
    agent = Agent()

    if command == 'random':
        agent.random_walk(state, DEFAULT_N)
    elif command == 'bfs':
        start_time = time.time()
        iterations = agent.bfs(state)

        print("Iterations needed: %s" % iterations)
        print("Time taken: %s seconds" % (time.time() - start_time))
    elif command == 'dfs':
        start_time = time.time()
        iterations = agent.dfs(state)

        print("Iterations needed: %s" % iterations)
        print("Time taken: %s seconds" % (time.time() - start_time))
    elif command == 'a_star':
        start_time = time.time()
        iterations = agent.a_star(state, heuristic)

        print("Iterations needed: %s" % iterations)
        print("Time taken: %s seconds" % (time.time() - start_time))
    else:
        print('Invalid command inputed')

if __name__ == "__main__":
	main()