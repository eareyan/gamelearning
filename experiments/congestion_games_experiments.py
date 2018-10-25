import matplotlib.pyplot as plt
import numpy as np
from algos import sampling
from structures import brg
import pandas as pd
from util.plot_lib import mean_confidence_interval

# from congestion.congestion_game_lib import congestionGame1
# congestionGame = congestionGame1

from congestion.congestion_games_factory import random_power_law_game

congestionGame = random_power_law_game


true_brg = brg.BRG.get_true_brg(congestionGame)
# brg.BRG.plot_graph(true_brg)

list_of_pureNash = brg.BRG.getListOfPureNash(congestionGame, true_brg)
print("There are " + str(len(list_of_pureNash)) + " pure Nash: ", list_of_pureNash)

"""
    Experiments for the simple sampling. 
"""
delta = 0.1
sample_increment = 50
length_of_grid = 10
numer_of_trials = 200

num_nash_means, num_nash_ub, num_nash_lb = [], [], []
eps_means, eps_ub, eps_lb = [], [], []
map_of_sampled_nash = {}
for t in range(1, length_of_grid + 1):
    num_samples = t * sample_increment
    print("\t experiment: ", t, ", numsamples = ", num_samples)
    num_nash_run_values, eps_run_values = [], []
    map_of_sampled_nash[num_samples] = {}
    for n in range(1, numer_of_trials + 1):
        # print("n = ", n)
        (eps, conf, dict_individual_estimated_eps_brgs) = sampling.simple_sampling(congestionGame, delta, num_samples)
        # Progressive sampling might need a different way of presenting results.
        # (num_samples, eps, delta_hat, conf, dict_individual_estimated_eps_brgs) = sampling.progressive_sampling(congestionGame, 2.8, delta, num_samples, 100000)
        list_of_sampled_pure_nashs = brg.BRG.getListOfPureNash(congestionGame, brg.BRG.merge_directed_graphs(dict_individual_estimated_eps_brgs))
        num_nash_run_values = num_nash_run_values + [len(list_of_sampled_pure_nashs)]
        eps_run_values = eps_run_values + [eps]
        for nash in list_of_sampled_pure_nashs:
            if nash not in map_of_sampled_nash[num_samples]:
                map_of_sampled_nash[num_samples][nash] = 0
            map_of_sampled_nash[num_samples][nash] = map_of_sampled_nash[num_samples][nash] + 1
    print(np.mean(num_nash_run_values), np.mean(eps_run_values))

    num_nash_mean, num_nash_lower, num_nash_upper = mean_confidence_interval(num_nash_run_values)
    num_nash_means, num_nash_ub, num_nash_lb = num_nash_means + [num_nash_mean], num_nash_ub + [num_nash_upper], num_nash_lb + [num_nash_lower]

    eps_mean, eps_lower, eps_upper = mean_confidence_interval(eps_run_values)
    eps_means, eps_ub, eps_lb = eps_means + [eps_mean], eps_ub + [eps_upper], eps_lb + [eps_lower]

print(map_of_sampled_nash)
""" Save a couple of plots. """
def getPlotTitle(title, numer_of_trials, congestionGame, list_of_pureNash):
    return "Random Power Law Game. \n" + str(title) \
           + str(numer_of_trials) + " trials." + "\n Players = " + str(congestionGame.numPlayers) + ", Facilities = " \
           + str(congestionGame.numFacilities) + ". Number of pure Nash: " + str(len(list_of_pureNash)) + "."

grid = [t * sample_increment for t in range(1, length_of_grid + 1)]

# Average number of nash plot
plt.fill_between(grid, num_nash_ub, num_nash_lb, color='g', alpha=.5)
plt.plot(grid, num_nash_means, color='g', linestyle='--')
plt.title(getPlotTitle("Avg. # of pure Nash equilibria as a function of # of samples, ", numer_of_trials, congestionGame, list_of_pureNash))
plt.xlabel("Number of samples")
plt.ylabel("Average number of Pure Nash")
plt.tight_layout()
plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/nash_plots/' + str(numer_of_trials) + '_num_nash_plot.png')

plt.clf()

# Average epsilon plot
plt.fill_between(grid, eps_ub, eps_lb, color='b', alpha=.5)
plt.plot(grid, eps_means, color='b', linestyle='--')
plt.title(getPlotTitle("Avg. # epsilon value as a function of # of samples, ", numer_of_trials, congestionGame, list_of_pureNash))
plt.xlabel("Number of samples")
plt.ylabel("Average epsilon")
plt.tight_layout()
plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/nash_plots/' + str(numer_of_trials) + '_eps_plot.png')

plt.clf()

# Histogram of nash frequencies
for m, map_of_nash in map_of_sampled_nash.items():
    df = pd.DataFrame({'Nash': [k for k in map_of_nash.keys()], 'Freq': [v for v in map_of_nash.values()]})
    df = df.sort_values('Freq', ascending=False)
    ax = df.plot.bar(x='Nash', y='Freq', rot=90, legend=None)
    plt.tight_layout()
    plt.xlabel("Strategy Profile")
    plt.ylabel("Frequency as a sampled Nash")
    plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/nash_plots/histogram-trials=' + str(
        numer_of_trials) + '-samples=' + str(m) + '.png')
    plt.clf()
