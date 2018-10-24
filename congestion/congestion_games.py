from structures import game, player
import itertools


class CongestionGame(game.Game):
    numFacilities = -1

    def __init__(self, name, num_players, num_facilities, strats, facilities_cost_functions):
        self.numPlayers = num_players
        self.numFacilities = num_facilities
        self.listOfPlayers = [player.Player(2) for i in range(0, num_players)]
        self.name = name
        self.payoffs = self.congestion_map_of_payoffs(num_players, strats, set([f for f in range(0, num_facilities)]),
                                                      facilities_cost_functions)

    def printGame(self, withPayoff):
        return super(CongestionGame, self).__str__() if withPayoff else \
            "Game: " + str(self.name) \
            + ". \n\t Players: \n\t\t" \
            + ('\n\t\t'.join(str(player) for player in self.listOfPlayers))

    def number_players_per_factory(self, profile, strats, facilities):
        """ count the number of players per factory in the given profile."""
        counts = {f: 0 for f in facilities}
        for p, s in strats.items():
            for f in s[profile[p]]:
                counts[f] += 1
        return counts

    def cost_profile_per_player(self, profile, strats, facilities, facilities_cost_functions):
        """compute the cost of each player for the profile"""
        congestion = self.number_players_per_factory(profile, strats, facilities)
        costs = {}
        p = 0
        for s in profile:
            costs[p] = sum([facilities_cost_functions[f](congestion[f]) for f in strats[p][s]])
            p += 1
        return costs

    def congestion_map_of_payoffs(self, num_players, strats, facilities, facilities_cost_functions):
        """compute the entire map of payoffs for the congestion game"""
        payoffs = {}
        for x in itertools.product(range(2), repeat=num_players):
            costs = self.cost_profile_per_player(x, strats, facilities, facilities_cost_functions)
            for p in range(0, num_players):
                # We negate costs since in congestion games players wish to minimize their cost as oppose to maximize their payoffs.
                payoffs[x + (p,)] = -1 * costs[p]
        return payoffs
