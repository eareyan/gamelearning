from congestion.congestion_games_factory import CongestionGamesFactory
from structures.game_factory import GameFactory
from algos.sampling import global_sampling
from structures.brg import BRG
from util.plot_lib import mean_confidence_interval
import pandas as pd
import matplotlib.pyplot as plt
from congestion.congestion_game_lib import simpleCongestionGame1


# Parameters
n, m, alpha = 3, 3, 0.75
delta = 0.1

number_trials = 150
final_list = []
# Evaluate a few number of samples to use in the simple sampling algorithm.
for t in range(1, 8):
    estimates = []
    num_samples = 50 * t
    print("t = ", t , ", num_samples = ", num_samples)
    for trials in range(0, number_trials):
        # Estimate the nash of the original game
        the_game = simpleCongestionGame1()
        #the_game = CongestionGamesFactory.create_power_law_game(n, m, alpha)
        list_or_pure_nash = BRG.getListOfPureNash(the_game, BRG.get_true_brg(the_game))
        (eps, conf, dict_individual_estimated_eps_brgs) = global_sampling(the_game, delta, num_samples)
        list_of_pure_estimated_nash = BRG.getListOfPureNash(the_game, BRG.merge_directed_graphs(dict_individual_estimated_eps_brgs))
        point_estimates = {k: v[0] + (eps / 2.0) for k, v in conf.items()}
        cost_of_nashs = {nash: sum([point_estimates[nash + (p,)] for p in range(0, the_game.numPlayers)]) for nash in list_of_pure_estimated_nash}
        worst_nash_estimated = min([v for k, v in cost_of_nashs.items()])
        #print(the_game)
        #print("The true Nashs: ", list_or_pure_nash)
        #print("The estimated Nash:", list_of_pure_estimated_nash)
        #print(point_estimates)
        #print("cost_of_nashs = " , cost_of_nashs)
        #print(worst_nash_estimated)

        #print("------------------------------")

        # Estimate the nash of the welfare game
        welfare_game = GameFactory.getWelfareGame(the_game)
        list_or_pure_nash_welfare = BRG.getListOfPureNash(welfare_game, BRG.get_true_brg(welfare_game))
        (eps_welfare, conf_welfare, dict_individual_estimated_eps_brgs_welfare) = global_sampling(welfare_game, delta, num_samples)
        list_of_pure_estimated_nash_welfare = BRG.getListOfPureNash(welfare_game, BRG.merge_directed_graphs(dict_individual_estimated_eps_brgs_welfare))
        optimal_estimated_welfare = max([v[0] + (eps_welfare / 2.0) for k, v in conf_welfare.items() if k[-1] == 0])
        estimates = estimates + [worst_nash_estimated / optimal_estimated_welfare]
        #print(welfare_game)
        #print("The true welfare Nashs: ", list_or_pure_nash_welfare)
        #print("The estimated welfare Nash:", list_of_pure_estimated_nash_welfare)
        #print(optimal_estimated_welfare)
        #print(eps_welfare, conf_welfare)
        #print(worst_nash_estimated / optimal_estimated_welfare)

    final_list = final_list + [(num_samples,) + mean_confidence_interval(estimates)]
data = pd.DataFrame(final_list, columns=['samples', 'mean', 'lower', 'upper'])
print(data)

plt.fill_between(data['samples'], data['upper'], data['lower'], color='g', alpha=.5)
plt.plot(data['samples'], data['mean'], color='g', linestyle='--')
plt.title('Estimated PoA as a function of number of samples')
plt.xlabel("Samples")
plt.ylabel("Average PoA over " + str(number_trials) + " trials")
plt.tight_layout()
plt.axhline(y=5.0 / 2.0, color='r', linestyle='-')  # Add a line with the ground truth value of POA, if available
#plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/nash_plots/' + str(numer_of_trials) + '_num_nash_plot.png')
plt.show()
