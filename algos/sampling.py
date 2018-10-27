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


def simple_sampling(game_input, delta, num_samples, HoeffdingIneq=False):
    """ Implements simple sampling algorithm """
    samples = game_input.get_noisy_samples(num_samples)
    # Compute confidence intervals for the entire game
    if HoeffdingIneq:
        (eps, conf) = rademacher.Rademacher.compute_confidence_intervals(samples, num_samples, delta, True, len(game_input.payoffs))
    else:
        (eps, conf) = rademacher.Rademacher.compute_confidence_intervals(samples, num_samples, delta)
    # Compute \hat{BRG}(\eps), i.e., the estimated epsilon BRG.
    dict_individual_estimated_eps_brgs = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(game_input, conf)
    return (eps, conf, dict_individual_estimated_eps_brgs)


def progressive_sampling(game_input, eps, delta, initial_num_samples, max_num_samples, HoeffdingIneq=False,
                         verbose=False):
    """ implements progressive sampling algorithm """
    i = 1
    n = math.floor(math.log((max_num_samples / initial_num_samples) + 1, 2))
    if verbose:
        print('n = ', n, ', target_eps = ', eps)
    while (True):
        num_samples = ((2 ** i) - 1) * initial_num_samples
        if verbose:
            print("num_samples = ", num_samples)
        if (num_samples > max_num_samples):
            return (None, None, None, None, None)
        else:
            (eps_t, conf_t, dict_individual_estimated_eps_brgs_t) = simple_sampling(game_input, delta / n, num_samples,
                                                                                    HoeffdingIneq)
            if verbose:
                print('eps_', i, ' = ', eps_t)
            if eps_t <= eps:
                if verbose:
                    print("found a BRG with required guarantess: eps = ", eps_t, ", delta = ", (i * (delta / n)))
                return (num_samples, eps_t, i * (delta / n), conf_t, dict_individual_estimated_eps_brgs_t)
        i = i + 1
