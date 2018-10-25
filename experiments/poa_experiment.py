from structures.game_factory import GameFactory
from structures.brg import BRG
from structures.game import Game
from congestion.congestion_games_factory import CongestionGamesFactory
from util.plot_lib import mean_confidence_interval
import pandas as pd



import matplotlib.pyplot as plt

data = pd.read_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/csv/poa.csv')
print(data)
plt.fill_between(data['alpha'], data['upper'], data['lower'], color='g', alpha=.5)
plt.plot(data['alpha'], data['mean'], color='g', linestyle='--')
plt.title('PoA as a function of alpha')
plt.xlabel("Alpha")
plt.ylabel("Average PoA")
plt.tight_layout()
#plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/nash_plots/' + str(numer_of_trials) + '_num_nash_plot.png')
plt.show()

exit()

def getWelfareMaxStrategy(welfare_game: Game):
    return max(welfare_game.payoffs.values())

print("Running poa experiment")
final_list = []

for t in range(0, 9):
    print("\t t = ", t)
    list_data = []
    for i in range(0, 1000):
        n = 5
        m = 5
        alpha = 0.1 * (1 + t)
        if i % 200 == 0:
            print("\t\t i = ", i, ", alpha = ", alpha)
        # Draw a game and get the value of the worst pure nash
        game = CongestionGamesFactory.create_power_law_game(n, m, alpha)
        list_or_pure_nash = BRG.getListOfPureNash(game, BRG.get_true_brg(game))
        worst_nash = min([game.get_sum_of_payoffs(nash) for nash in list_or_pure_nash])
        # Get the welfare max game and optimal welfare
        welfare_game = GameFactory.getWelfareGame(game)
        social_opt = getWelfareMaxStrategy(welfare_game)
        # Save results if the current run
        list_data = list_data + [worst_nash / social_opt]
    # Sort the results
    list_data.sort(reverse=True)
    # Append mean and bounds to list
    final_list = final_list + [(alpha,) + mean_confidence_interval(list_data)]

# Print some stuff and save a .csv
print(final_list)
data = pd.DataFrame(final_list, columns=['alpha', 'mean', 'lower', 'upper'])
data.to_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/csv/poa.csv')
print(data)
