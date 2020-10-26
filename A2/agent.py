import random
import rgb
from copy import deepcopy
import util

MAX_DFS_DEPTH = 10 # Set to 10 to avoid maximum recursion depth errors, found this depth limit to return the best results

def get_root_traversal_states(node, states = []):
    states.append(node.state)
    if node.parent == None:
        states.reverse()
        return states
    return get_root_traversal_states(node.parent, states)

class Node:
    state = None
    parent = None
    depth = 0
    possibleChildStates = None
    children = []

    def __init__(self, state):
        self.state = state
        self.possibleChildStates = state.actions()

    def __eq__(self, otherNode):
        if isinstance(otherNode, Node):
            return self.state == otherNode.state
    
    def getPossibleActions(self):
        return self.state.actions()

    def addChild(self, childNode):
        self.children.append(childNode)

    def setParent(self, parentNode):
        self.parent = parentNode
        self.depth = parentNode.depth + 1

class Agent:
    open = []
    closed = []
    searchType = ''
    heuristic = None
    maxDfsDepth = MAX_DFS_DEPTH

    def setMaxDfsDepth(self, depth):
        self.maxDfsDepth = depth

    def random_walk(self, state, n):
        currNode = Node(state)

        for _ in range(n - 1):
            nextNode = Node(deepcopy(currNode.state))          
            nextNode.setParent(currNode)
            
            childIndex = random.randint(0, len(nextNode.possibleChildStates) - 1)
            nextAction = nextNode.possibleChildStates[childIndex]
            nextNode.state.execute(nextAction)

            currNode.addChild(nextNode)
            currNode = nextNode

        states = get_root_traversal_states(currNode)
        util.pprint(states)

    def search(self, isBfs = True):
        goalNode = None
        currentDFSDepth = 0
        iterations = 0

        while self.open:
            node = self.open.pop(0)
            self.closed.append(node)
            if node.state.is_goal():
                goalNode = node
                break

            if self.searchType == 'dfs': 
                if currentDFSDepth <= self.maxDfsDepth:
                    currentDFSDepth += 1
                else:
                    currentDFSDepth = 0
                    continue

            for action in node.getPossibleActions():
                newNode = deepcopy(node)
                newNode.state.execute(action)
                iterations += 1

                if newNode not in self.closed or newNode not in self.open:
                    node.addChild(newNode)
                    newNode.setParent(node)
                    if self.searchType == 'bfs':
                        self.open.append(newNode)
                    elif self.searchType == 'dfs':
                        self.open.insert(0, newNode)
                    else:
                        self.open.append(newNode)
                        self.open.sort(key=lambda h: self.heuristic(h.state, h.depth))

        if goalNode:
            states = get_root_traversal_states(goalNode)
            util.pprint(states)
            return iterations
        else:
            print('Search failed, unable to find goal state.')
            return None


    def bfs(self, state):
        self.searchType = 'bfs'
        self.open.append(Node(state))
        return self.search()

    def dfs(self, state):
        self.searchType = 'dfs'
        self.open.append(Node(state))
        return self.search()

    def a_star(self, state, heuristic):
        self.searchType = 'astar'
        self.heuristic = heuristic
        self.open.append(Node(state))
        return self.search()

        