from tictactoe import Board, Trainer, Agent
import numpy as np
import time


def main():
    start_time = time.time()

    train = Trainer()
    train.load_serialize_file()

    # mytuple = tuple('-' for _ in range(9))
    # blankb = Board(mytuple)
    # board0 = blankb.add_move(0, 'X')
    # board1 = board0.add_move(1, 'O')
    # board2 = board1.add_move(4, 'X')
    # board3 = board2.add_move(6, 'O')
    # board4 = board3.add_move(8, 'X')
    # print('board4 winner? ', board4.has_winner())
    # print('board3 winner? ', board3.has_winner())
    # print('board2 winner? ', board3.has_winner())
    # print('board 4 winner is: ', board4.is_winner('0'))
    train.training(100000)
    train.save_table_to_file()
    train.save_table_as_csv()

    # save the win rate arrays and np arrays for import into matlab

    x_rate = train.win_rate_dataset_x
    o_rate = train.win_rate_dataset_o
    tie_rate = train.win_rate_dataset_tie
    epsilon_set = train.epsilon_dataset
    episode_num_set = train.current_episode_num_set

    np.savetxt('x_rate.csv', x_rate, delimiter=',')
    np.savetxt('o_rate.csv', o_rate)
    np.savetxt('tie_rate.csv', tie_rate)
    np.savetxt('epsilon_set.csv', epsilon_set)
    np.savetxt('episode_num_set.csv', episode_num_set)

    # make a list fo

    print("program complete. Total runtime: %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
