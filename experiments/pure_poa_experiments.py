from congestion import congestion_game_lib
from structures import game
from prob import rademacher
from util.plot_lib import mean_confidence_interval
import pandas as pd
import numpy as np

# file_location = '/Users/enriqueareyan/Documents/workspace/gamelearning/data/pure_poa/congestion_game.p'
# congestion_game = game.Game.read_game_from_file(file_location)
congestion_game = congestion_game_lib.simpleCongestionGame1()
# congestion_game = congestion_game_lib.simpleCongestionGame2()

print(congestion_game.get_size_of_game())
print("congestion_game = ", congestion_game)
print("True pure eq = ", congestion_game.get_pure_eps_nash())
print("PPOA = ", congestion_game.get_pure_price_of_anarchy())

exit()


def crazy_noise():
    if np.random.uniform(0, 1) < 0.5:
        return -3.0
    else:
        return 3.0


# noise_function = f = lambda: np.random.uniform(-0.00, 0.00)
noise_function = f = lambda: np.random.uniform(-5.0, 5.0)
# noise_function = f = lambda: np.random.uniform(0.00000000, 0.00000000)
# noise_function = crazy_noise
delta = 0.1
results = []
# Test epsilon-uniform approximations for various number of samples.
for num_samples in [i * 10 for i in range(1, 11)]:
    print("num_samples = ", num_samples)
    mean_0_results = []
    mean_2eps_results = []
    lb_results = []
    ub_results = []
    tlb_results = []
    # Fixing the number of samples, get a monte carlo estimate of the estimators.
    for t in range(0, 100):
        samples = congestion_game.get_noisy_samples(num_samples, noise_function)
        eps, means = rademacher.Rademacher.compute_confidence_intervals(samples=samples,
                                                                        m=num_samples,
                                                                        delta=delta,
                                                                        hoeffding_inequality=True,
                                                                        size_of_family=congestion_game.get_size_of_game(),
                                                                        return_only_means=True)
        estimated_game = game.Game("estimated Game", congestion_game.listOfPlayers, means)
        mean_0 = estimated_game.get_pure_price_of_anarchy(eps=0.0)
        mean_2eps = estimated_game.get_pure_price_of_anarchy(eps=eps)
        lb, ub = estimated_game.get_bounds_pure_price_of_anarchy(eps=eps)
        tlb = estimated_game.get_tighther_lb(eps=eps, gamma=1.5)
        mean_0_results += [mean_0]
        mean_2eps_results += [mean_2eps]
        lb_results += [lb]
        ub_results += [ub]
        tlb_results += [tlb]
    mean_0_mean, mean_0_lb, mean_0_ub = mean_confidence_interval(mean_0_results)
    mean_2eps_mean, mean_2eps_lb, mean_2eps_ub = mean_confidence_interval(mean_2eps_results)
    lb_mean, lb_lb, lb_ub = mean_confidence_interval(lb_results)
    up_mean, ub_lb, ub_ub = mean_confidence_interval(ub_results)
    tlb_mean, tlb_lb, tlb_ub = mean_confidence_interval(tlb_results)
    results += [
        [num_samples, mean_0_mean, mean_0_lb, mean_0_ub, mean_2eps_mean, mean_2eps_lb, mean_2eps_ub, lb_mean, lb_lb, lb_ub, up_mean, ub_lb, ub_ub, tlb_mean, tlb_lb, tlb_ub]]
print(results)
df = pd.DataFrame(results,
                  columns=['m',
                           'mean_0_mean', 'mean_0_lb', 'mean_0_ub',
                           'mean_2eps_mean', 'mean_2eps_lb', 'mean_2eps_ub',
                           'lb_mean', 'lb_lb', 'lb_ub',
                           'ub_mean', 'ub_lb', 'ub_ub',
                           'tlb_mean', 'tlb_lb', 'tlb_ub'])
print(df)

file_location = '/Users/enriqueareyan/Documents/workspace/gamelearning/data/pure_poa/resultsSimpleCongestionGame1.csv'
# file_location = '/Users/enriqueareyan/Documents/workspace/gamelearning/data/pure_poa/resultsSimpleCongestionGame2.csv'
df.to_csv(file_location, index=False)
