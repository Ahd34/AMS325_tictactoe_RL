import copy


class Board:

    def __init__(self, given_state: tuple):
        # constructor takes a tuple as the board representation
        # boards will be tuples because in order to be hashable, they need to be immutable
        # self.state = tuple('-' for _ in range(9))
        # if len(given_state) != 9:
        #     raise ValueError("State/Board must be of length 9.")
        # if any(char not in ['-', 'O', 'X'] for char in given_state):
        #     raise ValueError("Board must only contain '-', 'O', or 'X'")

        # if no errors, set the state and list of possible actions for the Board:
        self.state = given_state
        # testprint print("constructor: self.state: ", self.state)

        # create list of possible actions in the Board:
        self.possible_actions = []
        for index in range(len(self.state)):
            if self.state[index] == '-':
                self.possible_actions.append(index)



    def __repr__(self):
        rows = ["".join(str(elem) for elem in self.state[0:3]),
                "".join(str(elem) for elem in self.state[3:6]),
                "".join(str(elem) for elem in self.state[6:9])]
        return "\n".join(rows)

    def __eq__(self, other):
        return isinstance(self, Board) and self.state == other.state

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


    def add_move(self, index: int, player: str):
        """

        :param index:   which index a move is taking place
        :param player:  the player symbol to add to the board
        :return:        a new Board object with the added move

        """
        # self.state = tuple('-' for _ in range(9))
        # new_board_as_list = list(self.state)
        # new_board_as_list[index] = player
        new_board = self.state[:index] + (player,) + self.state[index+1:]
        # print("Board.add_move(): new_board: ", new_board, "\n")
        return Board(new_board)


    def has_winner(self):
        """
        Returns a boolean if the board contains a winner (True) or not (False)
        """
        # check rows
        for row in range(0, 9, 3): # for 0, 3, 6
            if self.state[row] != '-' and self.state[row] == self.state[row + 1] == self.state[row + 2]:
                # print('row winner, row: ', row, '\n')
                return True

        # check columns
        for j in range(0, 3, 1):
            if self.state[j] != '-' and self.state[j] == self.state[j + 3] == self.state[j + 6]:
                # print('j winner, j: ', j, '\n')
                return True

        # check diagonals
        if self.state[0] == self.state[4] == self.state[8] != '-':
            # print('diag 0 winner \n')
            return True
        if self.state[2] == self.state[4] == self.state[6] != '-':
            # print('diag 2 winner \n')
            return True

        return False

    def is_winner(self, player: str):
        """

        :param player: a character representing the player
        :return: boolean, true if player chr is the winner, false otherwise
        """
        if self.has_winner:
            # check the rows
            for row in range(0, 9, 3): #for 0, 3 and 6, the leading index of each row
                if player == self.state[row] == self.state[row + 1] == self.state[row + 2]:
                    return True
            # check columns
            for col in range(0,3): # 0, 1, and 2 are leading column indices
                if player == self.state[col] == self.state[col + 3] == self.state[col + 6]:
                    return True
            # check diagonals
            if player == self.state[0] == self.state[4] == self.state[8]:
                return True
            if player == self.state[2] == self.state[4] == self.state[6]:
                return True
        else:
            return False


    def has_tie(self):
        if self.has_winner():
            # print("board has a winner, so there not a tie.\n")
            return False

        elif len(self.possible_actions) == 0:
            # print("possible action list has len() 0, board has a tie.\n")
            return True
        else:
            # print("board does not have a winner and does not have a tie.\n")
            return False


