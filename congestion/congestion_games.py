from structures import game, player
import itertools


class CongestionGame(game.Game):
    num_facilities = -1
    #facilities_cost_functions = None
    strats = None
    facilities = None
    payoffs = None

    def __init__(self, name, num_players, num_facilities, strats, facilities_cost_functions):
        self.name = name
        self.num_players = num_players
        self.num_facilities = num_facilities
        self.strats = strats
        self.facilities_cost_functions = facilities_cost_functions
        self.facilities = set([f for f in range(0, num_facilities)])
        self.listOfPlayers = [player.Player(len(strats[i])) for i in range(0, num_players)]
        self.compute_congestion_map_of_payoffs()

    def print_game(self, with_payoff):
        """ A printer function. """
        return super(CongestionGame, self).__str__() if with_payoff else \
            "Game: " + str(self.name) \
            + ". \n\t Players: \n\t\t" \
            + ('\n\t\t'.join(str(player) for player in self.listOfPlayers))

    def number_players_per_factory(self, profile):
        """ count the number of players per factory in the given profile. """
        counts = {f: 0 for f in self.facilities}
        for p, s in self.strats.items():
            for f in s[profile[p]]:
                counts[f] += 1
        return counts

    def cost_profile_per_player(self, profile):
        """compute the cost of each player for the profile. """
        congestion = self.number_players_per_factory(profile)
        costs = {}
        p = 0
        for s in profile:
            costs[p] = sum([self.facilities_cost_functions[f](congestion[f]) for f in self.strats[p][s]])
            p += 1
        return costs

    def compute_congestion_map_of_payoffs(self):
        """compute the entire map of payoffs for the congestion game. """
        payoffs = {}
        for profile in itertools.product(*[[i for i in range(0, self.listOfPlayers[p].numActions)] for p in range(0, self.num_players)]):
            costs = self.cost_profile_per_player(profile)
            for p in range(0, self.num_players):
                # We negate costs since in congestion games players wish to minimize their cost as oppose to maximize their payoffs.
                payoffs[profile + (p,)] = -1 * costs[p]
        self.payoffs = payoffs

    def update_cost_functions(self, new_facilities_cost_functions):
        """ Updates the game with new facilities cost functions, but fixing all the players' strategies. """
        self.facilities_cost_functions = new_facilities_cost_functions
        self.compute_congestion_map_of_payoffs()
