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
            # print("assigning player ", self.symbol, ".")
        elif symbol_value == -1:
            self.symbol = 'O'
            # print("assigning player ", self.symbol, ".")
        else:
            raise ValueError("Invalid input. Player symbol must be either 1 or -1 to initialize")

    @staticmethod
    def get_behavior_action(state: Board, state_table: OrderedDict, epsilon) -> int:
        """
        called from trainer.py - returns a random action with probability epsilon
        :param state: Board object
        :param state_table: pass the state_table from Trainer
        :param epsilon: pass epsilon, which changes as num_episodes increases in Trainer
        :return: int action
        """
        # get valid action from the state table?
        # random_number = random.uniform(0, 1)
        # print('random num: ', random_number, ", ", epsilon, "\n")
        # action_table = state_table.get(state)
        if random.uniform(0, 1) < epsilon:
            # take a random action
            # print("take random action\n")
            return random.choice(state.possible_actions)
        else:
            # otherwise take an optimal action
            greedy_action = Agent.get_greedy_action(state, state_table)
            # print('take greedy action\n')
            return greedy_action

    @staticmethod
    def get_greedy_action(state: Board, state_table: OrderedDict[Board, OrderedDict]) -> int:
        """
        called from Trainer class.
        :param state: Board to get optimal action from.
        :param state_table: the Trainer.state_Table containing all action value pairs.
        :return: an int representing the action with the largest q value. If there is a tie, it will break randomly.
        """
        action_table = state_table[state]
        max_q = float('-inf')
        best_actions = []
        for key in action_table:
            if action_table[key] > max_q:
                max_q = action_table[key]
                best_actions.clear()
                best_actions.append(key)
            elif action_table[key] == max_q:
                best_actions.append(key)

        return random.choice(best_actions)
    @staticmethod
    def get_random_action(state: Board):
        pass
