from algos import psp
import numpy as np
import pandas as pd
from itertools import product
from prob import util_random
from congestion.congestion_games_factory import CongestionGamesFactory


delta = 0.1
initial_num_samples = 100
max_num_samples = 256000

results_df = pd.DataFrame([], columns=['c_noise', 'c_payoffs', 'algo', 'max_m', 'eps', 'delta', 'm', 'N_p', 'N_a',
                                       'N_gamma'])
results_list = []

t = 0
for m, c_noise, c_payoffs, num_players, num_actions in product([100, 200, 400, 800, 1600, 3200, 6400, 12800],
                                                               [1, 5, 10],
                                                               [1, 5, 10],
                                                               [2, 3, 4, 5],
                                                               [2, 3, 4, 5]):
    t += 1
    print(m, c_noise, c_payoffs, num_players, num_actions)
    noise_f = lambda: np.random.uniform(-c_noise / 2.0, c_noise / 2.0)

    #a_random_game = util_random.generate_random_game(num_players, num_actions, False,
    #                                                 rewards_function=lambda: np.random.uniform(-c_payoffs, c_payoffs))
    a_random_game = CongestionGamesFactory.create_random_power_law_game(num_players, num_actions, 0.1)

    total_num_samples, eps_t, delta_t, conf_t_before, dict_individual_estimated_eps_brgs, success = psp.psp(a_random_game,
                                                                                                            0.0,
                                                                                                            delta,
                                                                                                            initial_num_samples,
                                                                                                            m,
                                                                                                            HoeffdingIneq=True,
                                                                                                            verbose=False,
                                                                                                            noise_function=noise_f)
    sum_samples = sum([t for p, t in total_num_samples.items()])
    results_list += [(c_noise, c_payoffs, 'psp', m, eps_t, delta, sum_samples, num_players, num_actions,
                      a_random_game.get_size_of_game())]

partial_results_df = pd.DataFrame(results_list,
                                  columns=['c_noise', 'c_payoffs', 'algo', 'max_m', 'eps', 'delta', 'm', 'N_p', 'N_a',
                                           'N_gamma'])
results_df = pd.concat([results_df, partial_results_df])
results_df.to_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/hoeffding/test_plg.csv', index=False)
