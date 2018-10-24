#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:49:53 2018

@author: eareyanv
"""
import itertools
from prob import util_random


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
    numPlayers = -1
    payoffs = {}

    def __init__(self, name, listOfPlayers, payoffs):
        """ Constructor """
        self.name = name
        self.listOfPlayers = listOfPlayers
        self.numPlayers = len(self.listOfPlayers)
        # TODO: Check that the payoffs agree with number of players and their actions.
        # This check is easier to be implemented as a recursive function since there are
        # a variable number of players and a variable number of actions per player
        self.payoffs = payoffs

    def __str__(self):
        """ String representation of a game """
        return "Game: " + str(self.name) \
               + ". \n\t Players: \n\t\t" \
               + ('\n\t\t'.join(str(player) for player in self.listOfPlayers)) \
               + "\n\t Payoffs: \n\t\t" + str(self.payoffs)

    def get_max_payoff(self) -> float:
        """ Get the maximum payoff among all possible payoffs """
        return max(self.payoffs.items(), key=lambda e: e[1])[1]

    def get_neiborhood(self, strat_profile_player: tuple) -> list:
        """
            Given a tuple of strategy profile with player, returns the corresponding strategic neighbor as a list of 
            tuples of strategy profile with player.
            Note that the current implementation assume numbering between 0,...,n, for all components
            of the game: player, actions, etc. For example, the following 
            is a profile of a game with 3 players, where each player has four actions:
                (0, 1, 0, 2) where the last number denotes the player index.
                In this profile, player 0 and 2 play action 0, and player 1 playes action 1.
                This profile refers to the last player, player index 2.
        """
        i = strat_profile_player[self.numPlayers]
        neigh = []
        for a in range(0, self.listOfPlayers[i].numActions):
            strat = []
            for j in range(0, self.numPlayers):
                if j != i:
                    # Fix the actions of other players
                    strat.insert(j, strat_profile_player[j])
                else:
                    # Vary the actions of player i
                    strat.insert(j, a)
            # By convention, the last member of the tuple denotes the player to which this profile refers to.
            # TODO: perhaps refactor this such that we separate the strategy prpfile from the reference of a player.
            strat.insert(len(strat_profile_player), i)
            neigh += [tuple(x for x in strat)]
        return neigh

    def noisy_sample(self, strat_profile_player: tuple) -> float:
        """
        Generates a single noisy sample for the given complete strategy profile received as a tuple.
        """
        return self.payoffs[strat_profile_player] + util_random.get_noise()
        # return self.payoffs[strat_profile_player]

    def get_subset_noisy_samples(self, m: int, profiles: object) -> dict:
        """
        Generates m noisy samples of each strategy profile and player received as parameter.
        """
        return {strat_profile_player: [self.noisy_sample(strat_profile_player) for sample in range(0, m)]
                for strat_profile_player in profiles}

    def get_noisy_samples(self, m: int) -> dict:
        """ 
        Generates m noisy samples of each strategy profile and player of the game.
        """
        return {strat_profile_player: [self.noisy_sample(strat_profile_player) for sample in range(0, m)]
                for strat_profile_player, payoff in self.payoffs.items()}

    def get_other_strategies(self, player_index: int) -> list:
        """
        Given a player_index, generates all the strategies of all other players as a list of lists.
        """
        if player_index >= self.numPlayers:
            raise Exception(
                'Player index ' + str(player_index) + ' out of range, player index should be between 0 and ' + str(
                    self.numPlayers - 1))
        # Construct and return a list of lists with the cartesian product of all players' strategies except that of player_index
        return [list(other_strats)
                for other_strats in itertools.product(*[[a for a in range(0, self.listOfPlayers[j].numActions)]
                                                        for j in range(0, self.numPlayers) if j != player_index])]

    def get_zero_strategies(self, player_index: int) -> list:
        """
        Given a player index, return a list of all strategies profiles (with player) where player_index plays strategy zero.
        """
        profiles_other_strats = self.get_other_strategies(player_index)
        for s in profiles_other_strats:
            s.insert(player_index, 0)
            s.insert(self.numPlayers, player_index)
        # Add to the profile of other agents, the strategy 0 of the player and the player index at the end.
        return [tuple(s) for s in profiles_other_strats]
