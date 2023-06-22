import copy
from collections import OrderedDict
from typing import Type

from tictactoe import Board, Agent



class Trainer:
    # class variables:
    state_table: OrderedDict[Board, OrderedDict] = OrderedDict()
    player1 = Agent(1)
    player2 = Agent(-1)
    x_win_count = 0
    o_win_count = 0
    tie_count = 0
    currentEpisodeNum = 1

    currentPlayer = player1

    epsilon = 0.1
    blank_board = tuple('-' for _ in range(9))

    def __init__(self):
        # initialize an ordered dictionary. We need inner action tables, and outer state tables
        # self.state_table = OrderedDict()
        self.action_table = OrderedDict()

        # upon initialization of the trainer class, we will want to load a local state_table

    @staticmethod
    def training(num_episodes=10):
        # blank_board = tuple('-' for _ in range(9))
        current_state = Board(Trainer.blank_board)
        print('inside episode num ', ', of ', num_episodes, '\n')

        # set the players
        if Trainer.player1.symbol == 'X':
            player_x = Trainer.player1
            player_o = Trainer.player2
        else:
            player_x = Trainer.player2
            player_o = Trainer.player1

        # for each episode we want to play
        for episode in range(num_episodes):
            print('inside episode num ', episode, ', of ', num_episodes, '\n')
            epsilon = max(0.1, 0.9 + (episode / 1000000.0))
            # play a game
            winner = Trainer.training_one_episode(player_x, player_o, epsilon)

            if winner == 'X':
                print("X is the winner.\n")
                Trainer.x_win_count += 1
            elif winner == 'O':
                print("O is the winner.\n")
                Trainer.o_win_count += 1
            else:
                print("There is a tie.\n")
                Trainer.tie_count += 1

    @staticmethod
    def training_one_episode(player_x: Agent, player_o: Agent, epsilon):
        # initialize an empty Board called "board"
        state_x_t = Board(Trainer.blank_board)
        print(state_x_t)

        # make sure the board is in the state_table
        Trainer.add_state_to_state_table(state_x_t)

        # get an action from the player
        action_x_t = player_x.get_behavior_action(state_x_t, Trainer.state_table, epsilon)

        # update the board with the player's move
        current_state = state_x_t.add_move(action_x_t, player_x)

        # add the new board to the state table
        Trainer.add_state_to_state_table(current_state)

        # set state o_t to the latest board that X made a move on
        state_o_t = current_state.__deepcopy__()
        action_o_t = player_o.get_behavior_action(state_o_t, Trainer.state_table, epsilon)

        # while loop to play through the episode, break when there is a winner or tie
        while True:
            current_state = current_state.add_move(action_o_t, player_o)
            Trainer.add_state_to_state_table(current_state)
            # check if O ended the game
            if current_state.has_tie():
                reward_x, reward_o = 0, 0
                break
            elif current_state.is_winner('O'):
                reward_x = -1
                reward_o = 1
                break
            else:
                reward_x = 0
                reward_o = 0

            state_x_t_1 = copy.deepcopy(current_state)
            action_x_t_1 = player_x.get_behavior_action(state_x_t_1, Trainer.state_table, epsilon)

            # backup Q value for player x
            player_x.backup_q_value(state_x_t, action_x_t, state_x_t_1, reward_x, Trainer.state_table)

            # discard the history / move to next time step for X
            state_x_t = state_x_t_1
            action_x_t = action_x_t_1
            current_state = current_state.add_move(action_x_t, player_x)

            # check if X ended the game
            if current_state.has_tie():
                reward_x, reward_o = 0, 0
                break
            elif current_state.is_winner('X'):
                reward_x = 1
                reward_o = -1
                break
            else:
                reward_x = 0
                reward_o = 0

            state_o_t_1 = copy.deepcopy(current_state)
            action_o_t_1 = player_o.get_behavior_action(state_o_t_1, Trainer.state_table, epsilon)
            player_o.backup_q_value(state_o_t, action_o_t, state_o_t_1, reward_o)

            state_o_t = state_o_t_1
            action_o_t = action_o_t_1

        player_x.backup_q_value(state_x_t, action_x_t, state_x_t_1, reward_x)
        player_o.backup_q_value(state_o_t, action_o_t, state_o_t_1, reward_o)

        # return the winner
        if current_state.is_winner(player_x):

            return player_x.symbol
        elif current_state.is_winner(player_o):

            return player_o.symbol
        else:

            return '-'

    @staticmethod
    def add_state_to_state_table(state: Board):
        if state in Trainer.state_table.keys():
            return
        else:
            # create an action table with valid actions and default q-values of 0
            action_values = OrderedDict()
            for key in state.possible_actions():
                # default action value is 0
                action_values[key] = 0

            # add the action_values to the statetable as a value to the board as a key:

            Trainer.state_table[state] = action_values

    #def backup_q_value(self, state_s: Board, action_a: int, state_s_plus_1: Board, reward=0):
        # action_table = Trainer.state_table.get(state_s)






