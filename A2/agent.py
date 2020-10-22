import random
import rgb
from copy import deepcopy
import util

def get_root_traversal_states(node, states = []):
    states.append(node.state)
    if node.parent == None:
        states.reverse()
        return states
    return get_root_traversal_states(node.parent, states)

class Node:
    state = None
    parent = None
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

class Agent:
    open = []
    closed = []

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
        while self.open:
            node = self.open.pop(0)
            self.closed.append(node)
            if node.state.is_goal():
                goalNode = node
                break

            for action in node.getPossibleActions():
                newNode = deepcopy(node)
                newNode.state.execute(action)

                if newNode not in self.closed or newNode not in self.open:
                    node.addChild(newNode)
                    newNode.setParent(node)
                    if isBfs:
                        self.open.append(newNode)
                    else:
                        self.open.insert(0, newNode)
                
        states = get_root_traversal_states(goalNode)
        util.pprint(states)


    def bfs(self, state):
        self.open.append(Node(state))
        self.search()

    def dfs(self, state):
        self.open.append(Node(state))
        self.search(False)

    def a_star(self, state, heuristic):
        return

        