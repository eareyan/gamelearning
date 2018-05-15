#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 13:20:37 2018

@author: enriqueareyan
    Some experiments to test the first containment, i.e., if the true BRG is in \hat{BRG}(\eps)
"""
import brg
import sampling
import psp
#import test_games
import util_random

def brg_containments_checker(test_game, dict_individual_true_brgs, dict_individual_estimated_eps_brgs, dict_individual_2_eps_brgs):
    # For each player, check both contaiments: BRG \subseteq \hat{BRG}(\eps) \subseteq BRG(2\eps)
    for i in range(0, test_game.numPlayers):
        if not(brg.BRG.isG1ContainedInG2(dict_individual_true_brgs[i], dict_individual_estimated_eps_brgs[i])):
            return False
        if not(brg.BRG.isG1ContainedInG2(dict_individual_estimated_eps_brgs[i], dict_individual_2_eps_brgs[i])):
            return False
    return True


def test_simple_sampling(test_game, num_tests, delta, m):
    """ Run simple sampling sanity check """
    # Compute true BRG
    dict_individual_true_brgs = brg.BRG.construct_all_true_individual_restricted_brgs(test_game)
    counter = 0
    for t in range(0, num_tests):
        if(t % 50 == 0):
            print( 't = ', t)
        # Run the simple sampling algorithm. Get eps, conf, and the individuals BRG.
        (eps, conf, dict_individual_estimated_eps_brgs) = sampling.simple_sampling(test_game, delta, m)
        # Construct the estimated BRG. Here we construct all individual BRGs
        dict_individual_estimated_eps_brgs  = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(test_game, conf)
        # Compute true BRG(2*\eps)
        dict_individual_2_eps_brgs = brg.BRG.construct_all_true_individual_restricted_brgs(test_game, 2 * eps)
        if brg_containments_checker(test_game, dict_individual_true_brgs, dict_individual_estimated_eps_brgs, dict_individual_2_eps_brgs):
            counter = counter + 1
        else:
            break
    empirical_prob = counter / num_tests
    print('empirical probability of containment = ', empirical_prob)
    return empirical_prob

def test_progressive_sampling(test_game, num_tests, eps, delta, m, max_num_samples, which_algo):
    """ Run progressive sampling sanity check """
    # Compute true BRG
    dict_individual_true_brgs = brg.BRG.construct_all_true_individual_restricted_brgs(test_game)
    counter = 0
    failed_runs = 0
    for t in range(0, num_tests):
        if(t % 10 == 0):
            print( 't = ', t)
        # Run the progressive sampling algorithm. Get eps, conf, and the individuals BRG.
        if which_algo == 'progressive':
            (num_samples, eps_hat, delta_hat, conf, dict_individual_estimated_eps_brgs) = sampling.progressive_sampling(test_game, eps, delta, m, max_num_samples)
        # Run progressive sampling with prunning. Note that psp and progressive have the same input -> output signature.
        elif which_algo == 'psp':        
            (num_samples, eps_hat, delta_hat, conf, dict_individual_estimated_eps_brgs) = psp.psp(test_game, eps, delta, m, max_num_samples)
        else:
            raise Exception('Unknown algorithm ', which_algo)

        if num_samples is None:
            failed_runs = failed_runs + 1
            continue
        # Construct the estimated BRG. Here we construct all individual BRGs
        dict_individual_estimated_eps_brgs  = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(test_game, conf)
        # Compute true BRG(2*\eps)
        dict_individual_2_eps_brgs = brg.BRG.construct_all_true_individual_restricted_brgs(test_game, 2 * eps_hat)
        if brg_containments_checker(test_game, dict_individual_true_brgs, dict_individual_estimated_eps_brgs, dict_individual_2_eps_brgs):
            counter = counter + 1
        else:
            break
    empirical_prob = counter / (num_tests - failed_runs)
    print('empirical probability of containment = ', empirical_prob)
    print('fail runs =', failed_runs)
    return empirical_prob

# Parameters
num_experiments = 100
test_m = 100
test_delta = 0.2 # With probability at least 1 - delta, we get BRG \subseteq \hat{BRG}{\eps}
test_eps = 20.0
test_max_samples = test_m * 200
progressive_algo = 'progressive'
progressive_algo = 'psp'

# Get the game to experiment with from the library of games.
#experiment_game = test_games.get_prisonersDilemma()
#experiment_game = test_games.get_testGame()
#experiment_game = test_games.get_game3Players()

for e in range(1, num_experiments):
    print('e = ', e)
    # Generate a new game to experiment with.
    experiment_game = util_random.generate_random_game(3, 3, False)
    test_eps = abs(experiment_game.get_max_payoff() * 0.1)
    print('test_eps = ', test_eps)
    #empirical_prob = test_simple_sampling(experiment_game, num_experiments, test_delta, test_m)
    empirical_prob = test_progressive_sampling(experiment_game, num_experiments, test_eps, test_delta , test_m, test_max_samples, progressive_algo)
    if empirical_prob < 1 - test_delta:
        raise Exception('Ooops!, 1 - delta = ', (1 - test_delta) , ' > empirical_prob = ', empirical_prob)
        
    
# Note: The true BRG is not contained in the \hat{BRG}(\eps) if:
# game is 2 players, up to two actions, 
# and we don't have the noise condition in the rademacher calculation, 
# and the noise is 10000
# ALl of this might just mean that the epsilon is super big and thus,
# the estimated graph contains all edges! so we are estimating nothing
# need to think about how to test epsilons.