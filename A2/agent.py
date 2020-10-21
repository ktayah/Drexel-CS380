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

    # def search(self, state, is_dfs):
    #     print('initialState', state)
        
    #     if is_dfs:
    #         return
    #     else:
    #         root = Node(state)
    #         self.closed.append(root)
    #         self.open.append(root)
    #         if root.state.is_goal():
    #             return root
    #         i = 0
            
    #         while self.open and i < 10:
    #             i += 1
    #             node = self.open.pop(0)
    #             for possibleChildrenState in node.possibleChildStates:
    #                 newNode = Node(deepcopy(node.state))
    #                 node.addChild(newNode)
    #                 newNode.setParent(node)
    #                 newNode.state.execute(possibleChildrenState)
    #                 print('New interation', i)
    #                 print('newNode state', newNode.state)
    #                 for c in self.closed:
    #                     print(c.state)

    #                 if newNode not in self.closed:
    #                     if newNode.state.is_goal():
    #                         print('GoalState')
    #                         util.pprint(newNode.state)
    #                         return newNode
    #                     self.open.append(newNode)
    #             # level = []
    #             # for c in self.closed:
    #             #     level.append(c.state)
    #             # util.pprint(level)

    def bfs(self, state):
        self.search(state, False)

    def dfs(self, state):
        return

    def a_star(self, state, heuristic):
        return

        