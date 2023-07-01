from random import random

from tictactoe import Board, Agent, Trainer
from copy import copy


class TestTraining:

    def __init__(self, the_trainer, num_episodes=500000):
        """

        :type my_trainer: Trainer
        """
        self.win_rate_dataset_x = [0, 0, 0, 0]
        self.win_rate_dataset_o = [0, 0, 0, 0]
        self.win_rate_dataset_tie = [0, 0, 0, 0]
        self.win_count_x = 0
        self.win_count_o = 0
        self.win_count_tie = 0

        self.num_episodes_to_test = num_episodes
        self.blank_board = self.blank_board = Board(tuple('-' for _ in range(9)))
        self.trainer = the_trainer
        self.player1 = Agent(1)  # X
        self.player2 = Agent(-1)  # O

        for case in range(4):
            winner = str()

            for each_episode in range(self.num_episodes_to_test):

                if case == 0:
                    winner = self.play_random_vs_random()
                elif case == 1:
                    winner = self.play_agent_vs_random()
                elif case == 2:
                    winner = self.play_random_vs_agent()
                elif case == 3:
                    winner = self.play_agent_vs_agent()

                if winner == 'X':
                    self.win_count_x += 1
                elif winner == 'O':
                    self.win_count_o += 1
                elif winner == '-':
                    self.win_count_tie += 1

            # after all games are played for a case:
            self.win_rate_dataset_x[case] = copy(self.win_count_x)
            self.win_rate_dataset_o[case] = copy(self.win_count_o)
            self.win_rate_dataset_tie[case] = self.win_count_tie

            self.win_count_x = 0
            self.win_count_o = 0
            self.win_count_tie = 0


    def play_random_vs_random(self):
        current_state = self.blank_board
        # action = self.player1.get_random_action(current_state.possible_actions)
        while True:
            action = self.player1.get_random_action(current_state)
            # updating the board
            current_state = current_state.add_move(action, self.player1.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
            # otherwise continue now with player 2 moves
            action = self.player2.get_random_action(current_state)
            current_state = current_state.add_move(action, self.player2.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
        if current_state.is_winner(self.player1):
            return self.player1.symbol
        elif current_state.is_winner(self.player2):
            return self.player2.symbol
        elif current_state.has_tie():
            return '-'

    def play_agent_vs_random(self):
        current_state = self.blank_board
        while True:
            action = self.player1.get_greedy_action(current_state, self.trainer.state_table)
            # updating the board
            current_state = current_state.add_move(action, self.player1.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
            # otherwise continue now with player 2 moves
            action = self.player2.get_random_action(current_state)
            current_state = current_state.add_move(action, self.player2.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
        if current_state.is_winner(self.player1):
            return self.player1.symbol
        elif current_state.is_winner(self.player2):
            return self.player2.symbol
        elif current_state.has_tie():
            return '-'

    def play_random_vs_agent(self):
        current_state = self.blank_board
        while True:
            action = self.player1.get_random_action(current_state)
            # updating the board
            current_state = current_state.add_move(action, self.player1.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
            # otherwise continue now with player 2 moves
            action = self.player2.get_greedy_action(current_state, self.trainer.state_table)
            current_state = current_state.add_move(action, self.player2.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
        if current_state.is_winner(self.player1):
            return self.player1.symbol
        elif current_state.is_winner(self.player2):
            return self.player2.symbol
        elif current_state.has_tie():
            return '-'

    def play_agent_vs_agent(self):
        current_state = self.blank_board
        while True:
            action = self.player1.get_greedy_action(current_state, self.trainer.state_table)
            # updating the board
            current_state = current_state.add_move(action, self.player1.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
            # otherwise continue now with player 2 moves
            action = self.player2.get_greedy_action(current_state, self.trainer.state_table)
            current_state = current_state.add_move(action, self.player2.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
        if current_state.is_winner(self.player1):
            return self.player1.symbol
        elif current_state.is_winner(self.player2):
            return self.player2.symbol
        elif current_state.has_tie():
            return '-'




