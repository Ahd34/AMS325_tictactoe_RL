import tkinter as tk
from tkinter import ttk, messagebox


class TicTacToeGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tic-Tac-Toe')

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
        self.current_player = 'X'

        for i in self.buttons:
            for j in i:
                j.configure(text='')


game = TicTacToeGUI()

game.mainloop()
