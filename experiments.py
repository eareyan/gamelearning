#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 13:20:37 2018

@author: enriqueareyan
    Some experiments to test the first containment, i.e., if the true BRG is in \hat{BRG}(\eps)
"""
import test_games
from brg import BRG
import util_random
import sampling

def run_experiment(experiment_game, num_experiments, m, delta):
    """ Run experiments to test the performance of the simple sampling algorithm """
    # Compute true BRG
    dict_individual_true_brgs = BRG.construct_all_true_individual_restricted_brgs(experiment_game)
    # Counter
    counter = 0
    for t in range(0, num_experiments):
        if(t % 50 == 0):
            print( 't = ', t)
        # Run the simple sampling algorithm. Get eps, conf, and the individuals BRG.
        (eps, conf, dict_individual_estimated_eps_brgs) = sampling.simple_sampling(experiment_game, m, delta)
        # Construct the estimated BRG. Here we construct all individual BRGs
        dict_individual_estimated_eps_brgs  = BRG.construct_all_estimated_eps_individual_restricted_brgs(experiment_game, conf)
        # Compute true BRG(2*\eps)
        dict_individual_eps_brgs = BRG.construct_all_true_individual_restricted_brgs(experiment_game, 2*eps)
        # For each player, check both contaiments: BRG \subseteq \hat{BRG}(\eps) \subseteq BRG(2\eps)
        contaimentsHold = True
        for i in range(0, experiment_game.numPlayers):
            #print('Player ', i, ':', BRG.isG1ContainedInG2(dict_individual_true_brgs[i], dict_individual_estimated_eps_brgs[i]))
            if not(BRG.isG1ContainedInG2(dict_individual_true_brgs[i], dict_individual_estimated_eps_brgs[i])):
                contaimentsHold = False
                break
            if not(BRG.isG1ContainedInG2(dict_individual_estimated_eps_brgs[i], dict_individual_eps_brgs[i])):
                contaimentsHold = False
                break                
        if contaimentsHold:
            counter = counter + 1
            
    empirical_prob = counter / num_experiments
    print('empirical probability of containment = ', empirical_prob)
    return empirical_prob


# Parameters
num_experiments = 100
m = 100
delta = 0.45 # With probability at least 1-delta, we get BRG \subseteq \hat{BRG}{\eps}
# Get the game to experiment with
experiment_game = test_games.get_prisonersDilemma()
#experiment_game = test_games.get_testGame()
#experiment_game = test_games.get_game3Players()

for e in range(0,100):
    print('Random Game experiment')
    random_game = util_random.generate_random_game(2, 2)
    empirical_prob = run_experiment(random_game, num_experiments, m, delta)
    if empirical_prob < 1 - delta:
        raise Exception('Ooops!, 1 - delta = ', (1- delta) , ' > empirical_prob = ', empirical_prob)
        
    
# The true BRG is not contained in the \hat{BRG}(\eps) if:
# game is 2 players, up to two actions, 
# and we don't have the noise condition in the rademacher calculation, 
# and the noise is 10000
# ALl of this might just mean that the epsilon is super big and thus,
# the estimated graph contains all edges! so we are estimating nothing
# need to think about how to test epsilons.