import random
from collections import OrderedDict
import pickle
import csv
from tqdm import tqdm
from tictactoe import Board, Agent


class Trainer:
    # class variables:

    def __init__(self):

        self.state_table: OrderedDict[Board, OrderedDict] = OrderedDict()
        self.epsilon = 0.9
        self.alpha = 0.1
        self.gamma = 0.99
        self.currentEpisodeNum = 1
        self.x_win_count = 0.0
        self.o_win_count = 0.0
        self.tie_count = 0.0
        self.blank_board = Board(tuple('-' for _ in range(9)))
        self.player1 = Agent(1)
        self.player2 = Agent(-1)
        self.current_state = Board(tuple('-' for _ in range(9)))
        # establish data sets for plotting win rates over time in matlab as 3D
        # data sets will be x,y,z as : current_episode_number, current_epsilon, win_count/current_episode_num
        self.win_rate_dataset_x = []
        self.win_rate_dataset_o = []
        self.win_rate_dataset_tie = []
        self.epsilon_dataset = []
        self.current_episode_num_set = []
        self.add_state_to_state_table(self.current_state)


    def training(self, num_episodes=10):
        # blank_board = tuple('-' for _ in range(9))

        print('inside training() for ', num_episodes, ' episodes.\n')

        # set the players
        if self.player1.symbol == 'X':
            player_x = self.player1
            player_o = self.player2
        else:
            player_x = self.player2
            player_o = self.player1

        # for each episode we want to play

        for episode in tqdm(range(num_episodes), desc="Playing episodes."):
            # print('inside episode num ', episode, ', of ', num_episodes, '\n')
            self.epsilon = max(0.01, 0.9 - (episode / 500000.0))
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

            # after each episode, add the win rates, tie rates, and epsilon value to datasets for graphing
            self.win_rate_dataset_x.append(self.x_win_count / self.currentEpisodeNum)
            self.win_rate_dataset_o.append(self.o_win_count / self.currentEpisodeNum)
            self.win_rate_dataset_tie.append(self.tie_count / self.currentEpisodeNum)
            self.epsilon_dataset.append(self.epsilon)
            self.current_episode_num_set.append(self.currentEpisodeNum)

            self.currentEpisodeNum += 1

        # after all episodes, print the win counts
        print("X win count is: ", self.x_win_count)
        print("O win count is: ", self.o_win_count)
        print("Tie count is: ", self.tie_count)
        print("# of unique states encountered:", len(self.state_table))
        print("epsilon final value: ", self.epsilon)

    def training_one_episode(self, player_x: Agent, player_o: Agent, epsilon):
        # initialize an empty Board called "board"
        reward_x = 0.0
        reward_o = 0.0
        state_x_t = self.blank_board

        # get an action from the player
        action_x_t = player_x.get_behavior_action(state_x_t, self.state_table, epsilon)

        # update the board with the player's move
        self.current_state = state_x_t.add_move(action_x_t, player_x.symbol)
        state_o_t = self.current_state
        # print(current_state)
        self.add_state_to_state_table(self.current_state)

        action_o_t = player_o.get_behavior_action(state_o_t, self.state_table, epsilon)

        while True:
            self.current_state = self.current_state.add_move(action_o_t, player_o.symbol)
            # print(current_state)
            self.add_state_to_state_table(self.current_state)
            # check if O ended the game
            if self.current_state.is_winner(player_o.symbol):
                reward_x = -1.0
                reward_o = 1.0
                break
            elif self.current_state.has_tie():
                reward_x, reward_o = 0.0, 0.0
                break

            state_x_t_1 = self.current_state
            action_x_t_1 = player_x.get_behavior_action(self.current_state, self.state_table, epsilon)

            # backup Q value for player x
            self.backup_q_value(state_x_t, action_x_t, state_x_t_1, reward_x)

            # discard the history / move to next time step for X
            state_x_t = state_x_t_1
            action_x_t = action_x_t_1

            self.current_state = state_x_t.add_move(action_x_t, player_x.symbol)
            self.add_state_to_state_table(self.current_state)
            # print(current_state)

            # check if X ended the game
            if self.current_state.has_tie():
                reward_x, reward_o = 0.0, 0.0
                break
            elif self.current_state.is_winner(player_x.symbol):
                reward_x = 1.0
                reward_o = -1.0
                break

            state_o_t_1 = self.current_state
            action_o_t_1 = player_o.get_behavior_action(self.current_state, self.state_table, epsilon)
            self.backup_q_value(state_o_t, action_o_t, state_o_t_1, reward_o)

            # discard history, move to next time step for o
            state_o_t = state_o_t_1
            action_o_t = action_o_t_1

            # end of while loop

        self.backup_q_value(state_x_t, action_x_t, None, reward_x)
        self.backup_q_value(state_o_t, action_o_t, None, reward_o)

        # return the winner

        if reward_x == 1:
            return 'X'
        elif reward_o == 1:
            return 'O'
        else:
            return '-'
        # if current_state.is_winner(player_x.symbol):
        #
        #     return player_x.symbol
        # elif current_state.is_winner(player_o.symbol):
        #
        #     return player_o.symbol
        # else:
        #
        #     return '-'

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

    def backup_q_value(self, state_s: Board, action_a: int, state_s_plus_1=None, reward=0.0):
        """
        Q(s,a) = Q(s,a) + alpha * ( Reward + Y*argmax(s_t_plus_1) - Q(s,a))
        :param state_s: s
        :param action_a: a
        :param state_s_plus_1: s_1
        :param reward: 0 by default.
        :return: None. updates the self.state_table
        """
        action_table = self.state_table.get(state_s)
        action_table[action_a] = action_table[action_a] + self.alpha * (
                    reward + self.gamma * self.arg_max(state_s_plus_1) - action_table[action_a])

    def arg_max(self, state_s: Board):
        """
        gets the optimal q value of the given state.
        :param state_s: a Board object
        :return: float representing the highest Q-value in the action table for state_s
        """
        # check if the board is terminal?
        if state_s is None:
            return 0.0
        elif len(state_s.possible_actions) == 0:
            return 0.0
        else:
            # get the action table for the given state, check the q values and return the highest one.
            action_table: OrderedDict | list = self.state_table[state_s]

            q_values = action_table.values()
            max_q = max(q_values, default=0.0)

            # iterates over q_values and filters out any values that don't match max_q
            max_qty = [q for q in q_values if q == max_q]

            return random.choice(max_qty)

    def save_table_to_file(self):
        with open('state_table_serialized.pkl', 'wb') as file:
            pickle.dump(self.state_table, file)
            print("saving state_table to serialized file.")

    def load_serialize_file(self):
        try:
            with open('state_table_serialized.pkl', 'rb') as file:
                self.state_table = pickle.load(file)
                print("Loading serialized state_table file.")


        except FileNotFoundError:
            print("File not found. Generating blank state_table")

    def save_table_as_csv(self):
        # table_as_dataframe = pd.DataFrame.from_dict(self.state_table, orient='index')
        # table_as_dataframe.to_excel('state_table_excel.xlsx')
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['State', 'Action-Value Pairs'])
            for key, value in self.state_table.items():
                writer.writerow([key, [value.keys(), value.values()]])

    def clear_q_values(self):
        """
        sets the q-values for every state to 0.
        :return:
        """
        for key, value in self.state_table.items():
            for action in value:
                value[action] = 0.0
