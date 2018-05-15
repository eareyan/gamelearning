#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 09:44:05 2018

@author: enriqueareyan
"""
import rademacher
import brg
import math

def intersect_conf(conf1, conf2):
    """ Given two dict stratprofile -> conf_interval,
    intersect each of the confidence intervals corresponding to
    stratprofiles on both dicts and return a dic with the intersections.
    This function raises an exception in case some confidence intervals
    do not intersect.
    """
    finalConfs = {}
    for (profile, conf) in conf1.items():
        if profile in conf2:
            interConf = conf2[profile]
            # Check if the intersection is empty 
            if conf[1] < interConf[0] or conf[0] > interConf[1]:
                return None
                #raise Exception('Confidence intervals do not intersect')
            else:
                finalConfs[profile] = (max(conf[0], interConf[0]), min(conf[1], interConf[1]))
        else:
            finalConfs[profile] = conf1[profile]
    return finalConfs

def psp(game_input, eps, delta, initial_num_samples = 100, max_num_samples = 25600, HoeffdingIneq = False, verbose = False):
    """
    Implements progressive sampling with prunning. For now, just a doubling schedule.
    """
    # Collect an initial sample of all strat profile-player pairs
    (eps_t, conf_t_before) = rademacher.Rademacher.compute_confidence_intervals(game_input.get_noisy_samples(initial_num_samples), initial_num_samples, delta, HoeffdingIneq, len(game_input.payoffs))
    # Keep track of how many samples were taken for each strat profile-player pair
    total_num_samples = {s : initial_num_samples for (s,u) in game_input.payoffs.items()}
    # This function implements a doubling schedule. Compute the number of iterations.
    n = math.floor(math.log((max_num_samples / initial_num_samples) + 1, 2))
    if verbose:
        print('n = ', n, ', goal_eps = ', eps)
    pruneSet = set()
    for t in range(1, n + 1):
        delta_t = t * (delta / n)
        if verbose:
            print('eps_', t, ' = ', eps_t, ', delta_', t,' = ', delta_t)
        if(eps_t <= eps):
            if verbose:
                print('done at t = ', t)
            # Compute \hat{BRG}(\eps), i.e., the estimated epsilon BRG.
            dict_individual_estimated_eps_brgs  = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(game_input, conf_t_before)
            return (total_num_samples, eps_t, delta_t, conf_t_before, dict_individual_estimated_eps_brgs)
        keepList = []
        # For each player and each neighborhood
        for i in range(0, game_input.numPlayers):
            for strat in game_input.get_zero_strategies(i):
                (max_neigh, min_neigh) = brg.BRG.compute_max_min_neigh(game_input, strat, conf_t_before)
                pruneSet |= set(min_neigh)
                keepList += max_neigh                
        m = (2 ** (t - 1)) * initial_num_samples
        new_samples = game_input.get_subset_noisy_samples(m, keepList)
        (eps_t, conf_t_after) = rademacher.Rademacher.compute_confidence_intervals(new_samples, m, delta_t, HoeffdingIneq, len(keepList))
        conf_t_before = intersect_conf(conf_t_before, conf_t_after)
        if conf_t_before is None:
            return (None, None, None, None, None)
        # Collect number of samples each profile is sampled.
        for s in keepList:
            total_num_samples[s] = total_num_samples[s] + m
        if verbose:
            print('m = ', m, ', pruned so far = ', len(pruneSet))
    # If execution reaches this lines, then the algorithm failed.
    return (None, None, None, None, None)
    
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
            for neigh in game_input.get_neiborhood(s_0):
                print('\t', neigh,'\t', game_input.payoffs[neigh] , '\t', total_num_samples[neigh])
    max_num_samples = max(total_num_samples.items(), key = lambda e:e[1])[1]
    prc_worst_case_explored = sum(m for (s,m) in total_num_samples.items()) / (len(game_input.payoffs) * max_num_samples)
    print('Worst case explored up to: ', prc_worst_case_explored)
