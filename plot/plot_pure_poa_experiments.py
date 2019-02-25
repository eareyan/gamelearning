import pandas as pd
import matplotlib.pyplot as plt
import math


def compute_eps(size_of_family: int, delta: float, m: int):
    return 2.0 * math.sqrt((math.log((2.0 * size_of_family) / delta)) / (2.0 * m))


def plot_ppoa(file_location, true_ppoa, which_game):
    data = pd.read_csv(file_location)

    plt.fill_between(data['m'], data['mean_0_ub'], data['mean_0_lb'], color='blue', alpha=.5)
    plt.plot(data['m'], data['mean_0_mean'], color='blue', linestyle='--', label=r"0-$\epsilon$ estimator")  # ) label=r"$\hat{M}_0(\{\Gamma'_j\}_{j=1}^{100})$")

    plt.fill_between(data['m'], data['mean_2eps_ub'], data['mean_2eps_lb'], color='orange', alpha=.5)
    plt.plot(data['m'], data['mean_2eps_mean'], color='orange', linestyle='--', label=r"2-$\epsilon$ estimator")  # )label=r"$\hat{M}_{2\epsilon}(\{\Gamma'_j\}_{j=1}^{100})$")

    # ToDo: I have used label for upper bound here as congestion games are minimizing games not maximizing games.
    # ToDo: Note, we can actually compute this quantity analytically, no need for MC estimate here.
    # plt.fill_between(data['m'], data['lb_ub'], data['lb_lb'], color='red', alpha=.5)
    # plt.plot(data['m'], data['lb_mean'], color='red', linestyle='--', label=r"$\hat{U}(\{\Gamma'_j\}_{j=1}^{100})$")

    # ToDo: I have used label for lower bound here as congestion games are minimizing games not maximizing games.
    # ToDo: Note, we can actually compute this quantity analytically, no need for MC estimate here.
    # plt.fill_between(data['m'], data['ub_ub'], data['ub_lb'], color='green', alpha=.5)
    # plt.plot(data['m'], data['ub_mean'], color='green', linestyle='--', label=r"$\hat{L}(\{\Gamma'_j\}_{j=1}^{100})$")

    # Plot the actual value of the upper / lower bound estimators.
    if which_game == 1:
        plt.plot(data['m'], [(6.0 + 3.0 * compute_eps(24, 0.1, x)) / (6.0 - 3.0 * compute_eps(24, 0.1, x)) for x in data['m']], color='red', label=r"$U(\Gamma)$")
        plt.plot(data['m'], [(6.0 - 3.0 * compute_eps(24, 0.1, x)) / (15.0 + 3.0 * compute_eps(24, 0.1, x)) for x in data['m']], color='green', label=r"$L(\Gamma)$")

        # Experimenting with tighter bound for game 1
        plt.plot(data['m'], [(6.0 + 3.0 * compute_eps(24, 0.1, x)) / (15.0 - 3.0 * (compute_eps(24, 0.1, x)) + 3.0) for x in data['m']],
                 color='red', label=r"$U'(\Gamma), \gamma = 3$", linestyle=":")
    elif which_game == 2:
        plt.plot(data['m'], [(4.0 + 2.0 * compute_eps(16, 0.1, x)) / (4.0 - 2.0 * compute_eps(16, 0.1, x)) for x in data['m']], color='red', label=r"$U(\Gamma)$")
        plt.plot(data['m'], [(4.0 - 2.0 * compute_eps(16, 0.1, x)) / (4.0 + 2.0 * compute_eps(16, 0.1, x)) for x in data['m']], color='green', label=r"$L(\Gamma)$")

        # Experimenting with tighter bound for game 2
        plt.plot(data['m'], [(4.0 + 2.0 * compute_eps(24, 0.1, x)) / (4.0 - 2.0 * (compute_eps(24, 0.1, x)) + 1.0) for x in data['m']],
                 color='red', label=r"$U'(\Gamma), \gamma = 1$", linestyle=":")
    else:
        raise Exception("Unknown game")

    # plt.fill_between(data['m'], data['tlb_ub'], data['tlb_lb'], color='orange', alpha=.5)
    # plt.plot(data['m'], data['tlb_mean'], color='orange', linestyle='--', label=r"$\hat{L^*}(\{\Gamma'_j\}_{j=1}^{100})$")

    plt.axhline(true_ppoa, color='black', label=r'$A(\Gamma)$')
    plt.ylim(0.1, 2.5)
    plt.xlabel('Number of samples')
    if which_game == 1:
        plt.title("(a) Congestion game 1")
    elif which_game == 2:
        plt.title("(b) Congestion game 2")
    else:
        raise Exception("Unknown game")
    plt.legend()

    plt.show()


plt.rcParams.update({'font.size': 11., 'legend.loc': 'upper right'})
#plot_ppoa('/Users/enriqueareyan/Documents/workspace/gamelearning/data/pure_poa/resultsSimpleCongestionGame1.csv', 2.0 / 5.0, 1)
plot_ppoa('/Users/enriqueareyan/Documents/workspace/gamelearning/data/pure_poa/resultsSimpleCongestionGame2.csv', 1.0, 2)
