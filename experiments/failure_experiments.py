from prob import util_random
from algos import sampling
from structures import brg
from util.plot_lib import mean_confidence_interval
import pandas as pd
import numpy as np
from congestion import congestion_games_factory

print("Failure experiments")
# We fix the number of samples used by GS here.
num_samples = 100
# Structure of the results.
results_df = pd.DataFrame([], columns=['game', 'noise', 'discount', 'delta', 'mean', 'lower', 'upper'])

for num_games in range(0, 10):
    for g in [0, 1]:
        # Draw a random game.
        test_game = util_random.generate_random_game(3, 3) if g == 0 else congestion_games_factory.CongestionGamesFactory.create_random_power_law_game(3, 3, 0.5)
        # Compute true BRG.
        dict_individual_true_brgs = brg.BRG.construct_all_true_individual_restricted_brgs(test_game)
        print("\nuniform random game "  + str(num_games) if g == 0 else "\nfininte congestion game " + str(num_games))
        for discount_factor in [1.0, 0.875, 0.75, 0.625, 0.5]:
            print("")
            for noise_value in [5, 10, 50]:
                f = lambda: np.random.uniform(-noise_value / 2, noise_value / 2)
                final_list = []
                delta_grid = [i * 0.020 for i in range(1, 11)]
                for delta in delta_grid:
                    estimates = []
                    for t in range(0, 100):
                        print("\r \t\t discount_factor = " + str(discount_factor) + ", delta = " + str(delta) + ", t = " + str(t), end='')
                        # Run simple sampling.
                        (eps, conf, dict_individual_estimated_eps_brgs) = sampling.global_sampling(game_input=test_game,
                                                                                                   delta=delta,
                                                                                                   num_samples=num_samples,
                                                                                                   noise_function=f,
                                                                                                   discount_factor=discount_factor)
                        # Compute the true 2eps BRG.
                        dict_individual_2_eps_brgs = brg.BRG.construct_all_true_individual_restricted_brgs(test_game, 2.0 * eps)
                        # Check containments
                        first_containment = brg.BRG.brg_containment_checker(test_game, dict_individual_true_brgs, dict_individual_estimated_eps_brgs)
                        secon_containment = brg.BRG.brg_containment_checker(test_game, dict_individual_estimated_eps_brgs, dict_individual_2_eps_brgs)
                        estimates = estimates + ([1] if first_containment and secon_containment else [0])

                    final_list = final_list + [(g, noise_value, discount_factor, delta,) + mean_confidence_interval(estimates)]
                results = pd.DataFrame(final_list, columns=['game', 'noise', 'discount', 'delta', 'mean', 'lower', 'upper'])
                results_df = pd.concat([results_df, results])

print(results_df)
expt_id = util_random.id_generator()
print("Experiment id = " + str(expt_id))
results_df.to_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/prob_failure/' + expt_id + ".csv", index=False)
