import numpy as np
import pandas as pd
from algos import sampling
from structures import brg
from util.plot_lib import mean_confidence_interval
from congestion.congestion_games_factory import CongestionGamesFactory
from prob import util_random

# Create a random power law game. The game is fixed for the remainder of the experiments.
#a_random_game = CongestionGamesFactory.create_random_power_law_game(5, 5, 0.1)

# Create a random game.
a_random_game = util_random.generate_random_game(10, 2, False, noise_function=lambda: np.random.uniform(0.0, 0.5))

print(a_random_game)

# Compute the number of pure Nash in the fixed game.
true_brg = brg.BRG.get_true_brg(a_random_game)
# brg.BRG.plot_graph(true_brg)
list_of_pureNash = brg.BRG.getListOfPureNash(a_random_game, true_brg)
print("There are " + str(len(list_of_pureNash)) + " pure Nash: ", list_of_pureNash)

# Experiments for epsilon as a function of number of samples in global sampling.
delta = 0.1
sample_increment = 50
length_of_grid = 2
number_of_trials = 100

results_df = pd.DataFrame([], columns=['algo', 'noise', 'delta', 'num_samples', 'num_trials', 'num_nash_mean', 'num_nash_lower',
                                       'num_nash_upper', 'eps_mean', 'eps_lower', 'eps_upper'])
nash_df = pd.DataFrame([], columns=['algo', 'noise', 'num_samples', 'strategy', 'count'])
# Test Rademacher and Hoeffding
for hoeff in [False, True]:
    print("############ Testing " + ("Hoeffding" if hoeff else "Rademacher"))
    # Loop through all noise conditions.
    #for noise_c in [2, 5, 10]:
    for noise_c in [2]:
        #noise_f = lambda: np.random.uniform(-noise_c / 2, noise_c / 2)
        noise_f = lambda: 0.0
        num_nash_means, num_nash_ub, num_nash_lb = [], [], []
        eps_means, eps_ub, eps_lb = [], [], []
        map_of_sampled_nash = {}

        final_list = []
        print("Noise ->", noise_c)
        for t in range(1, length_of_grid + 1):
            num_samples = t * sample_increment
            num_nash_run_values, eps_run_values = [], []
            map_of_sampled_nash[num_samples] = {}
            for n in range(1, (number_of_trials + 1) if not hoeff else 3):
                # print("n = ", n)
                (eps, conf, dict_individual_estimated_eps_brgs) = sampling.global_sampling(a_random_game, delta,
                                                                                           num_samples,
                                                                                           hoeffding_inequality=hoeff,
                                                                                           noise_function=noise_f)
                # Progressive sampling might need a different way of presenting results.
                # (num_samples, eps, delta_hat, conf, dict_individual_estimated_eps_brgs) = sampling.progressive_sampling(congestionGame, 2.8, delta, num_samples, 100000)
                list_of_sampled_pure_nashs = brg.BRG.getListOfPureNash(a_random_game, brg.BRG.merge_directed_graphs(dict_individual_estimated_eps_brgs))
                num_nash_run_values = num_nash_run_values + [len(list_of_sampled_pure_nashs)]
                eps_run_values = eps_run_values + [eps]
                for nash in list_of_sampled_pure_nashs:
                    if nash not in map_of_sampled_nash[num_samples]:
                        map_of_sampled_nash[num_samples][nash] = 0
                    map_of_sampled_nash[num_samples][nash] = map_of_sampled_nash[num_samples][nash] + 1
            print("\t experiment: ", t, "\t numsamples = ", num_samples, "\t avg_num_nash = ", np.mean(num_nash_run_values), "\t avg_eps = ", np.mean(eps_run_values))

            # Compute statistitcs
            num_nash_mean, num_nash_lower, num_nash_upper = mean_confidence_interval(num_nash_run_values)
            eps_mean, eps_lower, eps_upper = mean_confidence_interval(eps_run_values)
            final_list += [("HF" if hoeff else "RC", noise_c, delta, num_samples, number_of_trials, num_nash_mean, num_nash_lower, num_nash_upper, eps_mean, eps_lower, eps_upper)]

        # Collect results about epsilon tolerance
        results = pd.DataFrame(final_list,
                               columns=['algo', 'noise', 'delta', 'num_samples', 'num_trials', 'num_nash_mean', 'num_nash_lower',
                                        'num_nash_upper', 'eps_mean', 'eps_lower', 'eps_upper'])
        results_df = pd.concat([results_df, results])

        # Collect results about frequency of pure Nash
        list_of_count_nash = [("HF" if hoeff else "RC", noise_c, num_samples, strat, count) for num_samples, map_of_nash in map_of_sampled_nash.items() for strat, count in map_of_nash.items()]
        nash_df = pd.concat([nash_df, pd.DataFrame(list_of_count_nash, columns=['algo', 'noise', 'num_samples', 'strategy', 'count'])])
print("final results= \n", results_df)

# Save datafiles with results.
expt_id = util_random.id_generator()
print("Experiment id = " + str(expt_id))
results_df.to_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/csv/epsilon/' + expt_id + '.csv', index=False)
nash_df.to_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/csv/epsilon/' + expt_id + '-nash.csv', index=False)
file = open('/Users/enriqueareyan/Documents/workspace/gamelearning/data/csv/epsilon/' + expt_id + '_meta.txt', 'w')
file.write(a_random_game.__str__() + "\n List of pure Nash: " + str(list_of_pureNash))
