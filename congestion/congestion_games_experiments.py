import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from algos import sampling
from structures import brg

from congestion.congestion_game_lib import congestionGame1
congestionGame = congestionGame1

#from congestion.congestion_games_factory import random_power_law_game
#congestionGame = random_power_law_game


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
    return m, m - h, m + h


# true_brg = brg.BRG.get_true_brg(congestionGame, eps=0.999)
# print(true_brg)
# brg.BRG.plot_graph(true_brg)

# pure_nash = brg.BRG.getListOfPureNash(congestionGame, true_brg)
# print("List of nashs: " , pure_nash)


"""
    Experiments for the simple sampling. 
"""
delta = 0.1
sample_increment = 50
length_of_grid = 10
numer_of_trials = 500

num_nash_means, num_nash_ub, num_nash_lb = [], [], []
eps_means, eps_ub, eps_lb = [], [], []
for t in range(1, length_of_grid + 1):
    num_samples = t * sample_increment
    print("Experiment: ", t, ", numsamples = ", num_samples)
    num_nash_run_values, eps_run_values = [], []
    for n in range(1, numer_of_trials):
        # print("n = ", n)
        (eps, conf, dict_individual_estimated_eps_brgs) = sampling.simple_sampling(congestionGame, delta, num_samples)
        # Progressive sampling might need a different way of presenting results.
        # (num_samples, eps, delta_hat, conf, dict_individual_estimated_eps_brgs) = sampling.progressive_sampling(congestionGame, 2.8, delta, num_samples, 100000)
        list_of_pure_nashs = brg.BRG.getListOfPureNash(congestionGame, brg.BRG.merge_directed_graphs(dict_individual_estimated_eps_brgs))
        num_nash_run_values = num_nash_run_values + [len(list_of_pure_nashs)]
        eps_run_values = eps_run_values + [eps]
    print(np.mean(num_nash_run_values), np.mean(eps_run_values))

    num_nash_mean, num_nash_lower, num_nash_upper = mean_confidence_interval(num_nash_run_values)
    num_nash_means, num_nash_ub, num_nash_lb = num_nash_means + [num_nash_mean], num_nash_ub + [
        num_nash_upper], num_nash_lb + [num_nash_lower]

    eps_mean, eps_lower, eps_upper = mean_confidence_interval(eps_run_values)
    eps_means, eps_ub, eps_lb = eps_means + [eps_mean], eps_ub + [eps_upper], eps_lb + [eps_lower]

""" Save a couple of plots. """
grid = [t * sample_increment for t in range(1, length_of_grid + 1)]

plt.fill_between(grid, num_nash_ub, num_nash_lb, color='g', alpha=.5)
plt.plot(grid, num_nash_means, color='g', linestyle='--')
plt.title("Average number of pure Nash equilibria \n as a function of number samples, using " + str(numer_of_trials) + " trials. \n Players = "
          + str(congestionGame.numPlayers) + ", Facilities = " + str(congestionGame.numFacilities)
          + ". Simple Game.")
plt.xlabel("Number of samples")
plt.ylabel("Average number of Pure Nash")
plt.tight_layout()
plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/nash_plots/' + str(numer_of_trials) + '_num_nash_plot.png')

plt.clf()

plt.fill_between(grid, eps_ub, eps_lb, color='b', alpha=.5)
plt.plot(grid, eps_means, color='b', linestyle='--')
plt.title("Average epsilon as a function of number samples, using " + str(numer_of_trials) + " trials. \n Players = "
          + str(congestionGame.numPlayers) + ", Facilities = " + str(congestionGame.numFacilities)
          + ". Simple Game.")
plt.xlabel("Number of samples")
plt.ylabel("Average epsilon")
plt.tight_layout()
plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/nash_plots/' + str(numer_of_trials) + '_eps_plot.png')
