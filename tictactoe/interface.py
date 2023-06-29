import pickle
import random

import tkinter as tk
from tkinter import ttk, messagebox

import board


class TicTacToeGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tic-Tac-Toe')

        self.actions = pickle.load(open('../state_table_serialized.pkl', 'rb'))
        self.state = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.buttons = []

        self.create_display()

    def create_display(self):
        frame = ttk.Frame(self)
        frame.pack()

        for i in range(3):
            row = []

            for j in range(3):
                button = ttk.Button(frame, text='', command=lambda row=i, col=j: self.move(row, col))
                button.grid(row=i, column=j)

                row.append(button)

            self.buttons.append(row)

    def move(self, row, col):
        if self.state[row][col] == '':
            self.state[row][col] = self.current_player

            self.buttons[row][col].configure(text=self.current_player)

            self.check_winner()

            self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            tk.messagebox.showinfo(title='Invalid Move', message='Please choose another space.')

        if self.current_player == 'O':
            agent_move = self.get_agent_move()

            self.move(agent_move[0], agent_move[1])

        print(self.get_agent_move())

    def check_winner(self):
        win_conditions = [self.state[0],
                          self.state[1],
                          self.state[2],
                          [self.state[i][0] for i in range(3)],
                          [self.state[i][1] for i in range(3)],
                          [self.state[i][2] for i in range(3)],
                          [self.state[i][i] for i in range(3)],
                          [self.state[i][2 - i] for i in range(3)]]

        for i in win_conditions:
            if i[0] == i[1] == i[2] != '':
                self.display_message(self.current_player)

        if all(self.state[i][j] != '' for i in range(3) for j in range(3)):
            self.display_message()

    def display_message(self, end_condition=None):
        if end_condition is None:
            tk.messagebox.showinfo(title='Game Over', message='Draw!')

            self.reset_game()
        else:
            tk.messagebox.showinfo(title='Game Over', message=f'Player {self.current_player} wins!')

            self.reset_game()

    def reset_game(self):
        self.state = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'O'

        for i in self.buttons:
            for j in i:
                j.configure(text='')

    def state_to_key(self):
        key = []

        for i in self.state:
            for j in i:
                if j == '':
                    key.append('-')
                else:
                    key.append(j)

        return tuple(key)

    def get_agent_move(self):
        translation = {0: (0, 0), 1: (0, 1), 2: (0, 2),
                       3: (1, 0), 4: (1, 1), 5: (1, 2),
                       6: (2, 0), 7: (2, 1), 8: (2, 2)}
        key = board.Board(self.state_to_key())

        try:
            vals = dict(self.actions[key])
            agent_move = max(vals, key=vals.get)

            return translation[agent_move]
        except KeyError:
            spaces = []

            for i in range(3):
                for j in range(3):
                    if self.state[i][j] == '':
                        spaces.append((i, j))

            agent_move = random.choice(spaces)

            return agent_move


game = TicTacToeGUI()

game.mainloop()
