import numpy as np
from congestion import congestion_games


class CongestionGamesFactory:

    @staticmethod
    def get_random_strategy(m, alpha):
        if m <= 0:
            raise Exception("there needs to be at least one factory")
        strat = []
        # We don't want to consider the empty strategy.
        while len(strat) == 0:
            for f in range(0, m):
                r = np.random.rand()
                if r <= (alpha ** (f + 1)):
                    strat += [f]
        return set(strat)

    @staticmethod
    def check_repeat_strategy(strategy, dict_strategies):
        for i, s in dict_strategies.items():
            if strategy == s:
                return True
        return False

    @staticmethod
    def create_power_law_game(n, m, alpha):
        facilities = set([i for i in range(0, m)])
        facilities_cost_functions = {i: lambda x: x for i in range(0, m)}
        strats = {}
        for p in range(0, n):
            strats[p] = {}
            # We want exactly 2 distinct strategies - have to think how this affect the strategies for small alpha
            while len(strats[p]) != 2:
                strat = CongestionGamesFactory.get_random_strategy(m, alpha)
                if not CongestionGamesFactory.check_repeat_strategy(strat, strats[p]):
                    strats[p][len(strats[p])] = strat
        return congestion_games.CongestionGame("random power law congestion game", n, m, strats, facilities_cost_functions)


n = 5
m = 5
alpha = 0.75

random_power_law_game = CongestionGamesFactory.create_power_law_game(n, m, alpha)
print(random_power_law_game.printGame(len(random_power_law_game.payoffs) <= 200))
print("Number of payoff entries = ", len(random_power_law_game.payoffs))
