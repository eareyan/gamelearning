#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 16:53:07 2018

@author: enriqueareyan
    Implements simple sampling and progressive sampling algorithms.
"""
from structures import brg
from prob import rademacher
import math


def global_sampling(game_input, delta, num_samples, hoeffding_inequality=False, noise_function=None, discount_factor=1.0):
    """ Implements global sampling algorithm """
    samples = game_input.get_noisy_samples(num_samples, noise_function)
    # Compute confidence intervals for the entire game
    (eps, conf) = rademacher.Rademacher.compute_confidence_intervals(samples=samples,
                                                                     m=num_samples,
                                                                     delta=delta,
                                                                     hoeffding_inequality=hoeffding_inequality,
                                                                     size_of_family=len(game_input.payoffs) if hoeffding_inequality else -1,
                                                                     discount_factor=discount_factor)
    # Compute \hat{BRG}(\eps), i.e., the estimated epsilon BRG.
    dict_individual_estimated_eps_brgs = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(game_input,
                                                                                                        conf)
    return eps, conf, dict_individual_estimated_eps_brgs


def progressive_sampling(game_input, eps, delta, initial_num_samples, max_num_samples, HoeffdingIneq=False,
                         verbose=False):
    """ implements progressive sampling algorithm """
    i = 1
    n = math.floor(math.log((max_num_samples / initial_num_samples) + 1, 2))
    if verbose:
        print('n = ', n, ', target_eps = ', eps, ', initial_num_samples = ', initial_num_samples, ', max_num_samples =',
              max_num_samples)
    while (True):
        num_samples = (2 ** (i - 1)) * initial_num_samples
        if (num_samples > max_num_samples):
            return (None, None, None, None, None)
        else:
            (eps_t, conf_t, dict_individual_estimated_eps_brgs_t) = global_sampling(game_input, delta / n, num_samples,
                                                                                    HoeffdingIneq)
            if verbose:
                print('num_samples = ', num_samples, ', eps_', i, ' = ', eps_t)
            if eps_t <= eps:
                if verbose:
                    print('found a BRG with required guarantess: eps = ', eps_t, ', delta = ', (i * (delta / n)))
                return (num_samples, eps_t, i * (delta / n), conf_t, dict_individual_estimated_eps_brgs_t)
        i = i + 1
