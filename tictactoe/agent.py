from tictactoe import Board
from collections import OrderedDict
import random



class Agent:
    def __init__(self, symbol_value: int):
        """
        creates an Agent with -1 representing X and 1 representing O
        :param symbol_value: integer 1 for X symbol and -1 for O symbol
        """
        alpha = 0.1
        gamma = 0.9

        # this part could be shortened
        if symbol_value == 1:
            self.symbol = 'X'
            print("assigning player ", self.symbol, ".")
        elif symbol_value == -1:
            self.symbol = 'O'
            print("assigning player ", self.symbol, ".")
        else:
            raise ValueError("Invalid input. Player symbol must be either 1 or -1 to initialize")

    @staticmethod
    def get_greedy_action(state: Board, state_table) -> int:
        action_table = state_table[state]
        max_q = float('-inf')
        best_actions = []
        for action in action_table.keys():
            if action_table[action] > max_q:
                max_q = action_table[action]
                best_actions.clear()
                best_actions.append(action)
            elif action_table[action] == max_q:
                best_actions.append(action)

        return random.choice(best_actions)

    @staticmethod
    def get_behavior_action(state: Board, state_table: OrderedDict, epsilon) -> int:
        """

        :param state: Board object
        :param state_table: pass the state_table from Trainer
        :param epsilon: pass epsilon, which changes as num_episodes increases in Trainer
        :return: int action
        """
        # get valid action from the state table?
        random_number = random.uniform(0, 1)
        action_table = state_table[state]
        if random_number >= epsilon:
            # take a random action
            return random.choice(action_table.keys())
        else:
            # otherwise take an optimal action
            greedy_action = Agent.get_greedy_action(state)
            return greedy_action

