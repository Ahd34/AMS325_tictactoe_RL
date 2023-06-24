import copy
import random
from collections import OrderedDict
from typing import Type

from tictactoe import Board, Agent





class Trainer:
    # class variables:

    def __init__(self):
        self.state_table: OrderedDict[Board, OrderedDict] = OrderedDict()
        self.epsilon = 0.9
        self.alpha = 0.1
        self.gamma = 0.99
        self.currentEpisodeNum = 1
        self.x_win_count = 0
        self.o_win_count = 0
        self.tie_count = 0
        self.blank_board = tuple('-' for _ in range(9))
        self.player1 = Agent(1)
        self.player2 = Agent(-1)

    def training(self, num_episodes=10):
        # blank_board = tuple('-' for _ in range(9))
        current_state = Board(self.blank_board)
        print('inside training() for ', num_episodes, ' episodes.\n')

        # set the players
        if self.player1.symbol == 'X':
            player_x = self.player1
            player_o = self.player2
        else:
            player_x = self.player2
            player_o = self.player1

        # for each episode we want to play
        for episode in range(num_episodes):
            # print('inside episode num ', episode, ', of ', num_episodes, '\n')
            self.epsilon = max(0.1, 0.9 - (episode / 1000000.0))
            # play a game
            winner = self.training_one_episode(player_x, player_o, self.epsilon)

            if winner == 'X':
                # print("X is the winner.\n")
                self.x_win_count += 1
            elif winner == 'O':
                # print("O is the winner.\n")
                self.o_win_count += 1
            else:
                # print("There is a tie.\n")
                self.tie_count += 1

        # after all episodes, print the win counts
        print("X win count is: ", self.x_win_count)
        print("O win count is: ", self.o_win_count)
        print("Tie count is: ", self.tie_count)
        print("# of unique states encountered:", len(self.state_table))
        print("epsilon final value: ", self.epsilon)

    def training_one_episode(self, player_x: Agent, player_o: Agent, epsilon):
        # initialize an empty Board called "board"

        state_x_t = Board(self.blank_board)
        # print(state_x_t)

        # make sure the board is in the state_table
        self.add_state_to_state_table(state_x_t)

        # get an action from the player
        action_x_t = player_x.get_behavior_action(state_x_t, self.state_table, epsilon)

        # update the board with the player's move
        current_state = state_x_t.add_move(action_x_t, player_x.symbol)
        # print(current_state)

        # add the new board to the state table
        self.add_state_to_state_table(current_state)

        # set state o_t to the latest board that X made a move on
        state_o_t = copy.deepcopy(current_state)
        action_o_t = player_o.get_behavior_action(state_o_t, self.state_table, epsilon)

        # while loop to play through the episode, break when there is a winner or tie
        while True:
            current_state = current_state.add_move(action_o_t, player_o.symbol)
            # print(current_state)
            self.add_state_to_state_table(current_state)
            # check if O ended the game
            if current_state.is_winner(player_o.symbol):
                reward_x = -1
                reward_o = 1
                break
            elif current_state.has_tie():
                reward_x, reward_o = 0, 0
                break
            else:
                reward_x = 0
                reward_o = 0

            state_x_t_1 = copy.deepcopy(current_state)
            action_x_t_1 = player_x.get_behavior_action(state_x_t_1, self.state_table, epsilon)

            # backup Q value for player x
            self.backup_q_value(state_x_t, action_x_t, state_x_t_1, reward_x)

            # discard the history / move to next time step for X
            state_x_t = state_x_t_1
            action_x_t = action_x_t_1
            current_state = current_state.add_move(action_x_t, player_x.symbol)
            self.add_state_to_state_table(current_state)
            # print(current_state)

            # check if X ended the game
            if current_state.has_tie():
                reward_x, reward_o = 0, 0
                break
            elif current_state.is_winner(player_x.symbol):
                reward_x = 1
                reward_o = -1
                break
            else:
                reward_x = 0
                reward_o = 0

            state_o_t_1 = copy.deepcopy(current_state)
            action_o_t_1 = player_o.get_behavior_action(state_o_t_1, self.state_table, epsilon)
            self.backup_q_value(state_o_t, action_o_t, state_o_t_1, reward_o)

            state_o_t = state_o_t_1
            action_o_t = action_o_t_1

        self.backup_q_value(state_x_t, action_x_t, state_x_t_1, reward_x)
        self.backup_q_value(state_o_t, action_o_t, state_o_t_1, reward_o)

        # return the winner
        if current_state.is_winner(player_x.symbol):

            return player_x.symbol
        elif current_state.is_winner(player_o.symbol):

            return player_o.symbol
        else:

            return '-'

    def add_state_to_state_table(self, state: Board):

        if state in self.state_table:
            # print("state already exists in table. Not adding.\n")
            return
        else:
            # create an action table with valid actions and default q-values of 0
            action_values = OrderedDict()
            for key in state.possible_actions:
                # default action value is 0.0
                action_values[key] = 0.0

            # add the action_values to the state table as a value to the board as a key:
            # print("Adding state to table.\n")
            self.state_table[state] = action_values


    def backup_q_value(self, state_s: Board, action_a: int, state_s_plus_1: Board, reward=0):
        """
        Q(s,a) = Q(s,a) + alpha * ( Reward + Y*argmax(s_t_plus_1) - Q(s,a))
        :param state_s: s
        :param action_a: a
        :param state_s_plus_1: s_1
        :param reward: 0 by default.
        :return: None. updates the self.state_table
        """
        q_s_a = self.state_table.get(state_s)
        q_s_a[action_a] = q_s_a[action_a] + \
            self.alpha * (reward + self.gamma * self.arg_max(state_s_plus_1) - q_s_a[action_a])

    def arg_max(self, state_s: Board):
        """
        gets the optimal q value of the given state.
        :param state_s: a Board object
        :return: float representing the highest Q-value in the action table for state_s
        """
        # check if the board is terminal?
        if len(state_s.possible_actions) == 0:
            return 0.0
        else:
            # get the action table for the given state, check the q values and return the highest one.
            action_table: OrderedDict | list = self.state_table[state_s]

            q_values = action_table.values()
            max_q = max(q_values, default=0)

            # iterates over q_values and filters out any values that don't match max_q
            max_qty = [q for q in q_values if q == max_q]

            return random.choice(max_qty)

