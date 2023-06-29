from tictactoe import Board, Trainer, Agent
import numpy as np
import time


def main():
    start_time = time.time()

    train = Trainer()
    train.load_serialize_file()

    train.clear_q_values()

    train.training(2000000)
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
