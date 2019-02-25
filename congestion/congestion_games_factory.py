import numpy as np
from congestion import congestion_games
from congestion.congestion_games import CongestionGame


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
    def create_random_power_law_game(n, m, alpha):
        # Currently, all cost functions are the identity function.
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

    @staticmethod
    def get_player_strats(m, how_many):
        memory = {}
        while len(memory) != how_many:
            s = np.random.choice(m, np.random.randint(1, m + 1), replace=False)
            s.sort()
            s = tuple(s)
            if s not in memory:
                memory[s] = True
        return {i: set(k) for i, (k, v) in enumerate(memory.items())}

    @staticmethod
    def get_random_congestion_game(n, m, facilities_cost_functions, ub_num_players_strats):
        # all_players_strats = {i: CongestionGamesFactory.get_player_strats(m, np.random.randint(1, ub_num_players_strats + 1)) for i in range(0, n)}
        all_players_strats = {i: CongestionGamesFactory.get_player_strats(m, ub_num_players_strats) for i in range(0, n)}
        return all_players_strats, CongestionGame("A random congestion game with " + str(m) + " facilities and ", n, m, all_players_strats, facilities_cost_functions)
