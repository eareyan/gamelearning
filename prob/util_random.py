#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:00:15 2018

@author: enriqueareyan
    Centralized file for all operations involving randomness.
"""

import numpy as np
import itertools
from structures import game, player
import random
import string

#noise_c = 5
#noise_c = 2
noise_c = 1
#random_game_noise_c = 100


def get_noise():
    return np.random.uniform(-noise_c / 2, noise_c / 2)

#def get_noise():
#    return np.random.normal(0, 1)


# def get_noise():
#    return -1 if np.random.uniform() <= 0.5  else 1

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_random_game(num_players, max_num_actions=2, random_num_actions=True):
    if random_num_actions:
        players_num_actions = [random.randint(1, max_num_actions) for i in range(0, num_players)]
    else:
        players_num_actions = [max_num_actions for i in range(0, num_players)]
    strat_profiles = [list(other_strats)
                      for other_strats in itertools.product(*[[a for a in range(0, players_num_actions[i])]
                                                              for i in range(0, len(players_num_actions))])]
    payoffs = {}
    for i in range(0, len(players_num_actions)):
        for s in strat_profiles:
            payoffs[tuple(s) + (i,)] = np.random.uniform(-random_game_noise_c / 2, random_game_noise_c / 2)
    listofplayers = [player.Player(n) for n in players_num_actions]
    return game.Game('Random Game', listofplayers, payoffs)
