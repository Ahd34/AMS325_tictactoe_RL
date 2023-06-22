import copy


class Board:

    def __init__(self, given_state: tuple):
        # constructor takes a tuple as the board representation
        # boards will be tuples because in order to be hashable, they need to be immutable
        # self.state = tuple('-' for _ in range(9))
        if len(given_state) != 9:
            raise ValueError("State/Board must be of length 9.")
        else:
            self.state = given_state
            print("constructor: self.state: ", self.state)

    def __repr__(self):
        rows = ["".join(str(elem) for elem in self.state[0:3]),
                "".join(str(elem) for elem in self.state[3:6]),
                "".join(str(elem) for elem in self.state[6:9])]
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


    def add_move(self, index: int, player: chr):
        """

        :param index:   which index a move is taking place
        :param player:  the player symbol to add to the board
        :return:        a new Board object with the added move

        """
        # self.state = tuple('-' for _ in range(9))
        # new_board_as_list = list(self.state)
        # new_board_as_list[index] = player
        new_board = self.state[:index] + (player,) + self.state[index+1:]
        return Board(new_board)

    def has_winner(self):
        """
        Returns a boolean if the board contains a winner (True) or not (False)
        """
        # check rows
        for row in range(0, 9, 3): # for 0, 3, 6
            if self.state[row] == self.state[row + 1] == self.state[row + 2]:
                print('row winner, row: ', row, '\n')
                return True
        # check columns
        for col in range(0): # for 0=3=6, 1=4=7, 2=5=8
            if self.state[col] == self.state[col + 3] == self.state[col + 6]:
                print('col winner, col: ', col, '\n')
                return True
        # check diagonals
        if self.state[0] == self.state[4] == self.state[8]:
            print('diag 0 winner \n')
            return True
        if self.state[2] == self.state[4] == self.state[6]:
            print('diag 2 winner \n')
            return True

        return False

    def is_winner(self, player: chr):
        '''

        :param player: a character representing the player
        :return: boolean, true if player chr is the winner, false otherwise
        '''
        if self.has_winner():
            # check the rows
            for row in range(0, 9, 3):
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
        """

        :return: list of possible actions for self
        """
        possible_actions = []
        for index in range(len(self.state)):
            if self.state[index] == '-':
                possible_actions.append(index)
        return possible_actions
