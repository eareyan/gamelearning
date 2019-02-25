#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:49:53 2018

@author: eareyanv
"""
import itertools
import math
from prob import util_random
import pickle
from structures.player import Player


class Game:
    """ A game represents a normal-form game.
    
    Attributes:
        name            A string human-readable game name
        listOfPlayers   A list with objects of type Player
        numPlayers      The total number of players
        payoffs         A dictionary {s : u_i} where s is a strategy profile (tuple)
                        with all players strategies AND the last entry is the index of the
                        player utility u_i refers to. Maybe would have been better to have
                        {s : {i : u_i}}, a potential code refactor opportunity. 
    """
    name = ''
    listOfPlayers = []
    num_players = -1
    payoffs = {}
    max_pure_welfare = -math.inf

    def __init__(self, name, listOfPlayers, payoffs):
        """ Constructor """
        self.name = name
        self.listOfPlayers = listOfPlayers
        self.num_players = len(self.listOfPlayers)
        # TODO: Check that the payoffs agree with number of players and their actions.
        # This check is easier to be implemented as a recursive function since there are
        # a variable number of players and a variable number of actions per player
        self.payoffs = payoffs

    def __str__(self):
        """ String representation of a game """
        return "Game: " + str(self.name) + " with " + str(self.num_players) + " players." \
               + "\n\t Players: \n\t\t" \
               + ('\n\t\t'.join(str(player) for player in self.listOfPlayers)) \
               + "\n\t Payoffs: \n\t\t" + str(self.payoffs) \
               + "\n\t Size of game:" + str(len(self.payoffs))

    def get_size_of_game(self):
        """ The size of the game is defined as the number of utility function that need to be estimated. """
        return len(self.payoffs)

    def get_max_payoff(self) -> float:
        """ Get the maximum payoff among all possible payoffs """
        return max(self.payoffs.items(), key=lambda e: e[1])[1]

    def get_neighborhood(self, strat_profile_player: tuple) -> list:
        """
            Given a tuple of strategy profile with player, returns the corresponding strategic neighbor as a list of tuples of strategy profile with player.
            Note that the current implementation assume numbering between 0,...,n-1, for all components of the game: player, actions, etc.
            For example, the following is a profile of a game with 3 players, where each player has four actions:
                (0, 1, 0, 2) where the last number denotes the player index.
                In this profile, player 0 and 2 play action 0, and player 1 plays action 1.
                This profile refers to the last player, player index 2.
        """
        i = strat_profile_player[self.num_players]
        neigh = []
        for a in range(0, self.listOfPlayers[i].numActions):
            strat = []
            for j in range(0, self.num_players):
                if j != i:
                    # Fix the actions of other players
                    strat.insert(j, strat_profile_player[j])
                else:
                    # Vary the actions of player i
                    strat.insert(j, a)
            # By convention, the last member of the tuple denotes the player to which this profile refers to.
            # TODO: perhaps refactor this such that we separate the strategy profile from the reference of a player.
            strat.insert(len(strat_profile_player), i)
            neigh += [tuple(x for x in strat)]
        return neigh

    def noisy_sample(self, strat_profile_player: tuple, noise_function=None) -> float:
        """
        Generates a single noisy sample for the given complete strategy profile received as a tuple.
        """
        return self.payoffs[strat_profile_player] + (util_random.get_noise() if noise_function is None else noise_function())
        # return self.payoffs[strat_profile_player]

    def get_noisy_strat_sample(self, m: int, strat_profile_player: tuple, noise_function=None) -> list:
        """
        Generates a list of noisy samples for a given strategy profile
        """
        return [self.noisy_sample(strat_profile_player, noise_function) for j in range(0, m)]

    def get_subset_noisy_samples(self, m: int, profiles: object, noise_function=None) -> dict:
        """
        Generates m noisy samples of each strategy profile and player received as parameter.
        """
        return {strat_profile_player: [self.noisy_sample(strat_profile_player, noise_function) for sample in range(0, m)]
                for strat_profile_player in profiles}

    def get_noisy_samples(self, m: int, noise_function=None) -> dict:
        """ 
        Generates m noisy samples of each strategy profile and player of the game.
        """
        return {strat_profile_player: [self.noisy_sample(strat_profile_player, noise_function) for k in range(0, m)] for strat_profile_player, payoff in self.payoffs.items()}

    def get_other_strategies(self, player_index: int) -> list:
        """
        Given a player_index, generates all the strategies of all other players as a list of lists.
        """
        if player_index >= self.num_players:
            raise Exception(
                'Player index ' + str(player_index) + ' out of range, player index should be between 0 and ' + str(self.num_players - 1))
        # Construct and return a list of lists with the cartesian product of all players' strategies except that of player_index
        return [list(other_strats)
                for other_strats in itertools.product(*[[a for a in range(0, self.listOfPlayers[j].numActions)]
                                                        for j in range(0, self.num_players) if j != player_index])]

    def get_zero_strategies(self, player_index: int) -> list:
        """
        Given a player index, return a list of all strategies profiles (with player) where player_index plays strategy zero.
        """
        profiles_other_strats = self.get_other_strategies(player_index)
        for s in profiles_other_strats:
            s.insert(player_index, 0)
            s.insert(self.num_players, player_index)
        # Add to the profile of other agents, the strategy 0 of the player and the player index at the end.
        return [tuple(s) for s in profiles_other_strats]

    def get_sum_of_payoffs(self, strategy: tuple):
        """
        Given a strategy, return the sum of the payoffs of all players in the strategy
        :param strategy:
        :return:
        """
        return sum([self.payoffs[strategy + (p,)] for p in range(0, self.num_players)])

    def get_max_pure_welfare(self):
        """
        Compute the maximum welfare among pure strategies
        :return:
        """
        if self.max_pure_welfare == -math.inf:
            all_strats = itertools.product(*[[i for i in range(0, self.listOfPlayers[p].numActions)] for p in range(0, self.num_players)])
            t = -math.inf
            for s in all_strats:
                accum = 0
                for p in range(0, self.num_players):
                    accum += self.payoffs[s + (p,)]
                if accum > t:
                    t = accum
            self.max_pure_welfare = t
        return self.max_pure_welfare

    def get_pure_eps_nash(self, eps=0.0):
        """
        Returns a list of pure Nash equilibria of the game
        :param eps:
        :return:
        """
        all_strats = itertools.product(*[[i for i in range(0, self.listOfPlayers[p].numActions)] for p in range(0, self.num_players)])
        pure_nash = {}
        list_pure_nash = []
        for s in all_strats:
            if s not in pure_nash:
                pure_nash[s] = True
            for p in range(0, self.num_players):
                if self.p_wants_to_deviate_at_s(s, p, eps):
                    pure_nash[s] = False
                    break
            if pure_nash[s]:
                list_pure_nash += [s]
        return list_pure_nash

    def p_wants_to_deviate_at_s(self, s, p, eps=0.0):
        """
        Returns true if player p wants to deviate at profile s up to 2eps tolerance.
        :param s:
        :param p:
        :param eps:
        :return:
        """
        for a in range(0, self.listOfPlayers[p].numActions):
            t = tuple([s[j] if j != p else a for j in range(0, self.num_players)])
            if t != s:
                if self.payoffs[s + (p,)] < self.payoffs[t + (p,)] - 2.0 * eps:
                    return True
        return False

    def get_bounds_pure_price_of_anarchy(self, eps=0.0):
        """
        Compute bounds on the eps-pure price of anarchy.
        :param eps:
        :return:
        """
        max_welfare = self.get_max_pure_welfare()
        list_of_pure_eq = [self.get_sum_of_payoffs(s) for s in self.get_pure_eps_nash(eps)]
        low_bound = (max_welfare - self.num_players * eps) / (max(list_of_pure_eq) + self.num_players * eps)
        up_bound = (max_welfare + self.num_players * eps) / (min(list_of_pure_eq) - self.num_players * eps)
        return low_bound, up_bound

    def get_tighther_lb(self, eps=0.0, gamma=0.0):
        """
        Compute a tigther lower bound
        :param eps:
        :param gamma:
        :return:
        """
        max_welfare = self.get_max_pure_welfare()
        list_of_pure_eq = [self.get_sum_of_payoffs(s) for s in self.get_pure_eps_nash(eps)]
        tight_low_bound = (max_welfare - self.num_players * eps) / (min(list_of_pure_eq) + self.num_players * (eps + gamma))
        return tight_low_bound

    def get_pure_price_of_anarchy(self, eps=0.0):
        """
        Compute the eps-pure price of anarchy
        :return:
        """
        max_welfare = self.get_max_pure_welfare()
        list_of_pure_eq = [self.get_sum_of_payoffs(s) for s in self.get_pure_eps_nash(eps)]
        worst_pure_eq = min(list_of_pure_eq)
        # if eps == 0.0 and len(list_of_pure_eq) > 1:
        #   print("\tfor eps = ", eps)
        #   print("\t list_of_pure_eq", list_of_pure_eq)
        #   exit()
        # else:
        #   print("NO")
        return max_welfare / worst_pure_eq

    def save_game(self, file_location):
        with open(file_location, 'wb') as fp:
            pickle.dump({'name': self.name,
                         'players_actions': [self.listOfPlayers[i].numActions for i in range(0, self.num_players)],
                         'payoffs': self.payoffs},
                        fp,
                        protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def read_game_from_file(file_location):
        with open(file_location, 'rb') as fp:
            data = pickle.load(fp)
            return Game(data['name'], [Player(a) for a in data['players_actions']], data['payoffs'])
