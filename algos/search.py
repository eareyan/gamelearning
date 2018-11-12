from tests import test_games
from queue import PriorityQueue
import random
import math
from prob import util_random
import numpy as np
from congestion.congestion_games_factory import CongestionGamesFactory
from structures import brg


def compute_num_samples(eps_tol, delta_tol, size_of_game):
    return -1.0 * math.log(1.0 - (1.0 - delta_tol) ** (1.0 / size_of_game)) / (2 * eps_tol * eps_tol)


def check_eps_nash(eps, the_game, S, empirical_means):
    for p in range(0, the_game.numPlayers):
        for s in the_game.get_neighborhood(S + (p,)):
            if S + (p,) != s and empirical_means[S + (p,)] < empirical_means[s] - 2 * eps:
                # print("\t\t\t ", (S + (p,), ":", empirical_means[S + (p,)]), ", ", s, ":", empirical_means[s])
                return False
    return True


# the_game = test_games.get_prisonersDilemma()
# the_game = test_games.get_testGame()
# the_game = test_games.get_game3Players()
# the_game = test_games.get_game2Players()
the_game = util_random.generate_random_game(2, 3, random_num_actions=False)
#the_game = CongestionGamesFactory.create_random_power_law_game(3, 3, 0.1)
#the_game = test_games.get_epsNashGame()


print(the_game)

# Parameters of the search
eps = 0.5
delta = 0.1
m = compute_num_samples(eps, delta, len(the_game.payoffs))
m = math.ceil(m)
# Initial profile for the search. At the moment is deterministic at (0,0,...,0).
start_profile = tuple(0 for i in range(0, the_game.numPlayers))
# Priority queue
Q = PriorityQueue()
Q.put((0, start_profile))
# Visited set
V = set()
# Keep track of profiles currently in queue
current_in_Q = set()
current_in_Q.add(start_profile)
# Some statistics
total_num_states = 0
#noise_function = lambda: 0
noise_function = lambda: np.random.uniform(-1.0, 1.0)
# noise_function = lambda :2
# Map of estimates so far
empirical_means = {}
# empirical_means = {start_profile + (p,): the_game.get_noisy_strat_sample(m, start_profile + (p,), noise_function=noise_function) for p in range(0, the_game.numPlayers)}
print("To guaranteee \eps = ", eps, "we need m = ", math.ceil(m))
print("empirical_means = ", empirical_means)
eps_nash_set = set()
while not Q.empty():
    total_num_states += 1
    next_profile = Q.get()
    # print("next_profile = ", next_profile, current_in_Q)
    S = next_profile[1]
    V.add(S)
    current_in_Q.remove(S)
    print("S = ", S)
    for p in range(0, the_game.numPlayers):
        for s in the_game.get_neighborhood(S + (p,)):
            # Sample payoffs for all players in this profile that had not already been sampled
            if s not in empirical_means:
                empirical_means[s] = np.mean(the_game.get_noisy_strat_sample(m, s, noise_function))
            # If the neighboring profile has not already been visited and is not already in the queue, then queue it.
            if s[0:-1] not in V and s[0:-1] not in current_in_Q:
                # Add the priority value to be the lowest estimate
                Q.put((empirical_means[s] - eps, s[0:-1]))
                current_in_Q.add(s[0:-1])
    # Check if S is an eps-Nash. If it is, return.
    if check_eps_nash(eps, the_game, S, empirical_means):
        eps_nash_set.add(S)
        break

print("empirical_means = ", empirical_means)
print(len(empirical_means))

print(total_num_states)
print("Found this Nash ", (2 * eps), ": ", eps_nash_set)

# Compute the number of pure Nash in the fixed game.
true_brg = brg.BRG.get_true_brg(the_game)
# brg.BRG.plot_graph(true_brg)
list_of_pureNash = brg.BRG.getListOfPureNash(the_game, true_brg)
print("There are " + str(len(list_of_pureNash)) + " pure Nash: ", list_of_pureNash)
