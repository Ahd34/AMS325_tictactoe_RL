import copy
import random
import pickle
from collections import OrderedDict

class Board:

    def __init__(self, given_state=None):
        # default constructor makes a blank board
        if given_state is None:
            self.state = ['-'] * 9
        else:
            self.state = given_state
        # 0 represents a blank. 1 Represents an X, -1 represents an O

    def __repr__(self):
        rows = []
        for i in range(3):
            row = " ".join(str(elem) for elem in self.state[i:i + 3])
            rows.append(row)
        return "\n".join(rows)

    def __eq__(self, other):
        if isinstance(other, Board):
            return self.state == other.state

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}
        new_board = Board(copy.deepcopy(self.state, memo))
        return new_board

    def __hash__(self):
        return hash(self.state)

    def __getstate__(self):
        return {
            'state': self.state
        }

    def __setstate__(self, state):
        self.state = state['state']

    def get_state(self):
        return self.state

    def add_move(self, index: int, player: chr):
        new_list = self.state.copy()
        new_list[index] = player
        return Board(new_list)

    def has_winner(self):
        """
        Returns a boolean if the board contains a winner (True) or not (False)
        """
        # check rows
        for row in range(3):
            if self.state[row] == self.state[row + 1] == self.state[row + 2]:
                return True
        # check columns
        for col in range(3):
            if self.state[col] == self.state[col + 3] == self.state[col + 6]:
                return True
        # check diagonals
        if self.state[0] == self.state[4] == self.state[8]:
            return True
        if self.state[2] == self.state[4] == self.state[6]:
            return True

        return False

    def is_winner(self, player: chr):
        if self.has_winner():
            # check the rows
            for row in range(3):
                if player == self.state[row] == self.state[row + 1] == self.state[row + 2]:
                    return True
            # check columns
            for col in range(3):
                if player == self.state[col] == self.state[col + 3] == self.state[col + 6]:
                    return True
            # check diagonals
            if player == self.state[0] == self.state[4] == self.state[8]:
                return True
            if player == self.state[2] == self.state[4] == self.state[6]:
                return True
            return False
        else:
            return False

    def possible_actions(self):
        possible_actions = []
        for index in self.state:
            if self.state[index] == '-':
                possible_actions.append(index)

        return possible_actions


class Agent:
    def __init__(self, symbol_value: int):
        '''
        creates an Agent with -1 representing X and 1 representing O
        :param symbol:
        '''
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
    def get_greedy_action(state: Board) -> int:
        action_table = Trainer.state_table[state]
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
    def get_behavior_action(state: Board) -> int:
        # get valid action from the state table?
        random_number = random.uniform(0, 1)
        action_table = Trainer.state_table[state]
        if random_number >= Trainer.epsilon:
            # take a random action
            return random.choice(action_table.keys())
        else:
            # otherwise take an optimal action
            greedy_action = Agent.get_greedy_action(state)
            return greedy_action

    def backup_q_value(self, state_s: Board, action_a: int, state_s_plus_1: Board, reward):
        action_table = Trainer.state_table


class Trainer:
    # public static vars:
    state_table: OrderedDict[Board, OrderedDict] = OrderedDict()
    player1 = Agent(1)
    player2 = Agent(-1)
    x_win_count = 0
    o_win_count = 0
    tie_count = 0
    currentEpisodeNum = 1

    currentPlayer = player1

    epsilon = 0.1

    def __init__(self):
        # initialize an ordered dictionary. We need inner action tables, and outer state tables
        # self.state_table = OrderedDict()
        self.action_table = OrderedDict()

        # upon initialization of the trainer class, we will want to load a local state_table

    @staticmethod
    def training(num_episodes=10):
        current_state = Board()
        print('inside episode num ', ', of ', num_episodes, '\n')

        for episode in range(num_episodes):
            print('inside episode num ', episode, ', of ', num_episodes, '\n')
            if Trainer.player1.symbol == 'X':
                player_x = Trainer.player1
                player_o = Trainer.player2
            else:
                player_x = Trainer.player2
                player_o = Trainer.player1

            winner = Trainer.training_one_episode(player_x, player_o)
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
    def training_one_episode(player_x: Agent, player_o: Agent):
        # initialize an empty Board called "board"
        state_x_t = Board()
        current_state = state_x_t
        print(current_state)

        # make sure the board is in the state_table
        Trainer.add_state_to_state_table(state_x_t)

        # get an action from the player
        action_x_t = player_x.get_behavior_action(state_x_t)

        # update the board with the player's move
        current_state.add_move(action_x_t, player_x)

        # add the new board to the state table
        Trainer.add_state_to_state_table(current_state)

        # set state o_t to the latest board that X made a move on
        state_o_t = Board.__deepcopy__(current_state)
        action_o_t = player_o.get_behavior_action(state_o_t)

        # while loop to play through the episode
        while True:
            current_state.add_move(action_o_t, player_o)
            # check for a winner or tie
            if current_state.has_winner() or current_state.has_tie():
                reward_x = current_state.get_reward(player_x)
                reward_o = current_state.get_reward(player_o)
                Trainer.add_state_to_state_table(current_state)
                break
            else:
                reward_x = 0
                reward_o = 0
                Trainer.add_state_to_state_table(current_state)

            state_x_t_1 = current_state.__deepcopy__()
            action_x_t_1 = player_x.get_behavior_action(state_x_t_1)

            # backup Q value for player x
            player_x.backup_q_value(state_x_t, action_x_t, state_x_t_1, reward_x)

            state_x_t = state_x_t_1
            action_x_t = action_x_t_1
            current_state.add_move(action_x_t, player_x)

            if current_state.has_winner() or current_state.has_tie():
                reward_x = current_state.get_reward(player_x)
                reward_o = current_state.get_reward(player_o)
                Trainer.add_state_to_state_table(current_state)
                break
            else:
                reward_x = 0
                reward_o = 0
                Trainer.add_state_to_state_table(current_state)

            state_o_t_1 = current_state.__deepcopy__()
            action_o_t_1 = player_o.get_behavior_action(state_o_t_1)
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
        if state not in Trainer.state_table:
            # create an action table with valid actions and default q-values of 0
            action_values = OrderedDict()
            for key in state.possible_actions():
                # default action value is 0
                action_values[key] = 0

            # add the action_values to the statetable as a value to the board as a key:

            Trainer.state_table[state] = action_values






