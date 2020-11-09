from game import Player

class HumanPlayer(Player):
    def choose_action(self, state):
        actions = state.actions(self.token)
        actionIndex = 0

        for action in actions:
            print(str(actionIndex) + ': ' + str(action))
            actionIndex += 1
            
        value = int(input('Please choose an action:'))
        return actions[value]