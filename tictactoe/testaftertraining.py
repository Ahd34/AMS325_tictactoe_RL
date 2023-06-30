from random import random

from tictactoe import Board, Agent, Trainer


class TestTraining:

    def __init__(self, num_episodes=500000, trainer=Trainer):
        self.win_rate_dataset_x = []
        self.win_rate_dataset_o = []
        self.win_rate_dataset_tie = []
        self.num_episodes_to_test = num_episodes
        self.blank_board = self.blank_board = Board(tuple('-' for _ in range(9)))
        self.trainer = trainer
        self.player1 = Agent(1)  # X
        self.player2 = Agent(-1)  # O

        for episode in range(self.num_episodes_to_test):
            self.play_random_vs_random()

    def play_random_vs_random(self):
        current_state = self.blank_board
        #action = self.player1.get_random_action(current_state.possible_actions)
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
            current_state = current_state.add_move(action)
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
            action = self.player1.get_greedy_action(current_state)
            # updating the board
            current_state = current_state.add_move(action, self.player1.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
            # otherwise continue now with player 2 moves
            action = self.player2.get_random_action(current_state)
            current_state = current_state.add_move(action)
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
            action = self.player2.get_greedy_action(current_state)
            current_state = current_state.add_move(action)
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
            action = self.player1.get_greedy_action(current_state)
            # updating the board
            current_state = current_state.add_move(action, self.player1.symbol)
            if current_state.has_tie():
                break
            elif current_state.has_winner():
                break
            # otherwise continue now with player 2 moves
            action = self.player2.get_greedy_action(current_state)
            current_state = current_state.add_move(action)
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
        return



