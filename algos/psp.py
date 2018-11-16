#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 09:44:05 2018

@author: enriqueareyan
"""
from structures import brg
from prob import rademacher
import math


def intersect_conf(conf1, conf2):
    """ Given two dict stratprofile -> conf_interval,
    intersect each of the confidence intervals corresponding to
    stratprofiles on both dicts and return a dic with the intersections.
    This function raises an exception in case some confidence intervals
    do not intersect.
    """
    final_confs = {}
    for (profile, conf) in conf1.items():
        if profile in conf2:
            inter_conf = conf2[profile]
            # Check if the intersection is empty 
            if conf[1] < inter_conf[0] or conf[0] > inter_conf[1]:
                return None
                # raise Exception('Confidence intervals do not intersect')
            else:
                final_confs[profile] = (max(conf[0], inter_conf[0]), min(conf[1], inter_conf[1]))
        else:
            final_confs[profile] = conf1[profile]
    return final_confs


def psp(game_input, eps, delta, initial_num_samples=100, max_num_samples=25600, HoeffdingIneq=False, verbose=False, noise_function=None):
    """
    Implements progressive sampling with prunning. For now, just a doubling schedule.
    """
    # This function implements a doubling schedule. Compute the number of iterations.
    n = math.floor(math.log((max_num_samples / initial_num_samples) + 1, 2))
    inner_delta = delta / n
    # Collect an initial sample of all strat profile-player pairs
    (eps_t, conf_t_before) = rademacher.Rademacher.compute_confidence_intervals(game_input.get_noisy_samples(initial_num_samples, noise_function), initial_num_samples, inner_delta, HoeffdingIneq, game_input.get_size_of_game())
    if verbose:
        print('delta at each call of global sampling = ', inner_delta)
        print('num_samples = ', initial_num_samples, '\t eps_', 0, ' = ', eps_t, '\t pruned so far = ', 0)
    # Keep track of how many samples were taken for each strat profile-player pair
    total_num_samples = {s: initial_num_samples for (s, u) in game_input.payoffs.items()}
    if verbose:
        print('n = ', n, ', target_eps = ', eps, ', initial_num_samples = ', initial_num_samples, ', max_num_samples =', max_num_samples)
    prune_set = set()
    for t in range(1, n + 1):
        delta_t = t * (delta / n)
        if eps_t <= eps:
            # Compute \hat{BRG}(\eps), i.e., the estimated epsilon BRG.
            if verbose:
                print('Able to find guarantees')
            dict_individual_estimated_eps_brgs = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(game_input, conf_t_before)
            return total_num_samples, eps_t, delta_t, conf_t_before, dict_individual_estimated_eps_brgs, True
        keep_list = []
        # For each player and each neighborhood
        for i in range(0, game_input.numPlayers):
            for strategy in game_input.get_zero_strategies(i):
                (max_neigh, min_neigh) = brg.BRG.compute_max_min_neigh(game_input, strategy, conf_t_before)
                prune_set |= set(min_neigh)
                keep_list += max_neigh
        num_samples = (2 ** t) * initial_num_samples
        new_samples = game_input.get_subset_noisy_samples(num_samples, keep_list, noise_function)
        (eps_t, conf_t_after) = rademacher.Rademacher.compute_confidence_intervals(new_samples, num_samples, inner_delta, HoeffdingIneq, len(keep_list))
        conf_t_before = intersect_conf(conf_t_before, conf_t_after)
        if conf_t_before is None:
            if verbose:
                print("Failed to intersect confidence intervals, abort. ")
            return total_num_samples, eps_t, delta_t, conf_t_before, None, False
        # Collect number of samples each profile is sampled.
        for s in keep_list:
            total_num_samples[s] = total_num_samples[s] + num_samples
        if verbose:
            #print(keep_list, num_samples)
            print('num_samples = ', num_samples, '\t eps_', t, ' = ', eps_t, '\t keep_list_len =', len(keep_list), '\t pruned so far = ', len(prune_set))

    if eps_t <= eps:
        if verbose:
            print('done at t = ', t)
        # Compute \hat{BRG}(\eps), i.e., the estimated epsilon BRG.
        dict_individual_estimated_eps_brgs = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(game_input, conf_t_before)
        return total_num_samples, eps_t, delta_t, conf_t_before, dict_individual_estimated_eps_brgs, True
    else:
        # If execution reaches this lines, then the algorithm failed.
        return total_num_samples, eps_t, delta_t, conf_t_before, None, False

    # If there is no active profile across all profiles
    # but epsilon is not as small as wanted by the user, then what?
    # Keep sampling until we get the right guarantess
    #
    # NOT SURE THE FOLLOWING IS TRUE:
    # Also, if there is only one profile active AND the epsilon
    # guarantee is meet, THEN stop sampling THIS profile.
    # Otherwise, we cannot claim an eps-best response.
    # Recall that intersection of profiles make it so that we
    # no longer have uniform size of intervals across all active profiles.
    #
    # As implemented, epsilon might go up as I compute
    # rademacher complexity BEFORE intersecting... is this right?
    # Feels like epsilons check are a bit more delicate
    # if we want the best algorithm possible.
    # For now, checking epsilon before intersecting is suboptimal
    # but it is correct, i.e., preserves guarantees. 


def inspect_psp_output(total_num_samples, game_input):
    """
    A function to output some useful statistics about psp.
    For manual inspection only.
    """
    for i in range(0, game_input.numPlayers):
        for s_0 in game_input.get_zero_strategies(i):
            print(s_0)
            for neigh in game_input.get_neighborhood(s_0):
                print('\t', neigh, '\t', game_input.payoffs[neigh], '\t', total_num_samples[neigh])
    max_num_samples = max(total_num_samples.items(), key=lambda e: e[1])[1]
    prc_worst_case_explored = sum(m for (s, m) in total_num_samples.items()) / (
            len(game_input.payoffs) * max_num_samples)
    print('Worst case explored up to: ', prc_worst_case_explored)
