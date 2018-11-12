from prob import util_random
from algos import sampling
from structures import brg
from util.plot_lib import mean_confidence_interval
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from congestion import congestion_games_factory
# Draw a random game.
#test_game = util_random.generate_random_game(3, 3)
test_game = congestion_games_factory.CongestionGamesFactory.getRandomPowerLawGame(2, 2, 0.5)
# Compute true BRG.
dict_individual_true_brgs = brg.BRG.construct_all_true_individual_restricted_brgs(test_game)
print(test_game)

# We fix the number of samples here
num_samples = 200
results_df = pd.DataFrame([], columns=['noise', 'delta', 'mean', 'lower', 'upper'])
for noise_value in [5, 10, 50]:
    # f = lambda: np.random.uniform(0, noise * 10)
    f = lambda: np.random.uniform(-noise_value / 2, noise_value / 2)
    final_list = []
    delta_grid = [i * 0.020 for i in range(1, 26)]
    print("\n noise_value = ", noise_value)
    for delta in delta_grid:
        estimates = []
        for t in range(0, 100):
            print("\r \t\t delta = " + str(delta) + ", t = " + str(t), end='')
            # Run simple sampling.
            (eps, conf, dict_individual_estimated_eps_brgs) = sampling.global_sampling(test_game, delta, num_samples,
                                                                                       noise_function=f)
            # Compute the true 2eps BRG.
            dict_individual_2_eps_brgs = brg.BRG.construct_all_true_individual_restricted_brgs(test_game, 2.0 * eps)
            # Check containments
            first_containment = brg.BRG.brg_containment_checker(test_game, dict_individual_true_brgs,
                                                                dict_individual_estimated_eps_brgs)
            secon_containment = brg.BRG.brg_containment_checker(test_game, dict_individual_estimated_eps_brgs,
                                                                dict_individual_2_eps_brgs)
            estimates = estimates + ([1] if first_containment and secon_containment else [0])

        final_list = final_list + [(noise_value, delta,) + mean_confidence_interval(estimates)]
    results = pd.DataFrame(final_list, columns=['noise', 'delta', 'mean', 'lower', 'upper'])
    results_df = pd.concat([results_df, results])

print(results_df)
expt_id = util_random.id_generator()
print("Experiment id = " + str(expt_id))
results_df.to_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/prob_failure/' + expt_id + ".csv",
                  index=False)

# plot = True
# Plot
# if plot:
# expt_id = 'Y3OFEM'
expt_data = pd.read_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/prob_failure/' + expt_id + '.csv')

colors = ['g', 'b', 'r', 'y', 'o']
n = 0
for i, r in expt_data.groupby('noise').sum().iterrows():
    data = expt_data[expt_data['noise'] == i]
    plt.fill_between(data['delta'], data['upper'], data['lower'], color=colors[n], alpha=.5)
    plt.plot(data['delta'], data['mean'], color=colors[n], linestyle='--', label='noise ' + str(i))
    plt.title('Empirical failure probability as a function of ' + r'$\delta$' + '\n using ' + str(num_samples) + ' samples per run of simple algorithm')
    plt.xlabel(r'$\delta$')
    plt.ylabel("Empirical failure")
    plt.plot([0, 0.5], [1, 0.5], 'k-')
    plt.tight_layout()
    plt.legend()
    plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/prob_failure/' + expt_id + '_plot.png')
    n += 1
plt.show()
