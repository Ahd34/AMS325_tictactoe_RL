# loadserialzedfile
# resetQValues()
# initialize chart data variables
import tictactoe
from tictactoe import Board, Trainer, Agent

def main():
#     myTrainer = Trainer()
    mytuple = tuple('-' for _ in range(9))
    blankb = Board(mytuple)
    board0 = blankb.add_move(0, 'x')
    board1 = board0.add_move(1, 'o')
    board2 = board1.add_move(4, 'x')
    board3 = board2.add_move(6, 'o')
    board4 = board3.add_move(8, 'x')
    print('board4 winner? ', board4.has_winner())
    print('board3 winner? ', board3.has_winner())
    print('board2 winner? ', board3.has_winner())
    print('board 4 winner is: ', board4.is_winner('0'))
    Trainer.training(10)

if __name__ == '__main__':
    main()





