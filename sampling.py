#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 16:53:07 2018

@author: enriqueareyan
    Implements simple sampling and progressive sampling algorithms.
"""
from rademacher import Rademacher
from brg import BRG
import math

def simple_sampling(game_input, num_samples, delta):
    """ Implements simple sampling algorithm """
    # Compute confidence intervals for the entire game
    (eps, conf) = Rademacher.compute_confidence_intervals(game_input.get_noisy_samples(num_samples), num_samples, delta)
    # Compute \hat{BRG}(\eps), i.e., the estimated epsilon BRG.
    dict_individual_estimated_eps_brgs  = BRG.construct_all_estimated_eps_individual_restricted_brgs(game_input, conf)
    return (eps, conf, dict_individual_estimated_eps_brgs)


def progressive_sampling(game_input, eps, delta, initial_num_samples, max_num_samples):
    """ implements progressive sampling algorithm """
    i = 1
    n = math.floor(math.log((max_num_samples / initial_num_samples) + 1, 2))
    print('n = ' , n)
    while(True):
        num_samples = ((2 ** i)-1) * initial_num_samples
        if(num_samples > max_num_samples):
            return False
        else:
            (eps_t, conf_t, dict_individual_estimated_eps_brgs_t) = simple_sampling(game_input, num_samples, delta / n)
            print(eps_t)
            if eps_t <= eps:
                print("found a BRG with required guarantess: eps = " , eps_t , ", delta = ", (i * (delta / n)))
                return (eps_t, i * (delta / n), conf_t, dict_individual_estimated_eps_brgs_t)
        print("num_samples = ", num_samples)
        i = i + 1