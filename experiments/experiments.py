#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:42:26 2018

@author: enriqueareyan
"""
from prob import util_random
from algos import sampling, psp
import time
import pandas as pd
import sys

if len(sys.argv) == 3:
    # Read size of game from command line
    num_players = int(sys.argv[1])
    num_actions = int(sys.argv[2])
else:
    # Fixed size of game
    num_players = 2
    num_actions = 2
    
print('*** Run experiment: num_players = ', num_players, ' and num_actions = ', num_actions, '***')

# Generate a random game.
experiment_game = util_random.generate_random_game(num_players, num_actions, False)
# Parameters of the experiment
prc_grid =[0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
delta = 0.1
m = 100
max_num_samples = 100000
# Collect results in a datafarme
results = pd.DataFrame(columns = ['m','eps','time', 'algo', 'type'])
# Run experiments
for prc in range(0, len(prc_grid)):
    for t in range(0, 100):
        eps = abs(experiment_game.get_max_payoff() * prc_grid[prc]) 
        print('Run #', t, ' \t ', prc_grid[prc], ' \t eps = ', eps)
        
        # First run progressive sampling with Rademacher complexity
        start_time = time.time()
        (num_samples, eps_hat, delta_hat, conf, dict_individual_estimated_eps_brgs) = sampling.progressive_sampling(experiment_game, eps, delta, m, max_num_samples, False)
        total_time = time.time() - start_time
        if num_samples is not(None):
            total_samples = num_samples * len(experiment_game.payoffs)
            results = results.append({'m' : total_samples, 'eps' : prc_grid[prc], 'time' : total_time, 'algo' : 'ps', 'type' : 'rademacher'}, ignore_index = True)

        # Second run progressive sampling with Hoeffding's inequality
        start_time = time.time()
        (num_samples, eps_hat, delta_hat, conf, dict_individual_estimated_eps_brgs) = sampling.progressive_sampling(experiment_game, eps, delta, m, max_num_samples, True)
        total_time = time.time() - start_time
        if num_samples is not(None):
            total_samples = num_samples * len(experiment_game.payoffs)
            results = results.append({'m' : total_samples, 'eps' : prc_grid[prc], 'time' : total_time, 'algo' : 'ps', 'type' : 'hoeffding' }, ignore_index = True)

        # Third run psp with Rademacher complexity
        start_time = time.time()
        (num_samples, eps_hat, delta_hat, conf, dict_individual_estimated_eps_brgs) = psp.psp(experiment_game, eps, delta, m, max_num_samples, False)
        total_time = time.time() - start_time
        if num_samples is not(None):
            total_samples = sum(num_samples.values())
            results = results.append({'m' : total_samples, 'eps' : prc_grid[prc], 'time' : total_time, 'algo' : 'psp', 'type' : 'rademacher'}, ignore_index = True)

        # Fourth run psp with Hoeffding's inequality
        start_time = time.time()
        (num_samples, eps_hat, delta_hat, conf, dict_individual_estimated_eps_brgs) = psp.psp(experiment_game, eps, delta, m, max_num_samples, True)
        total_time = time.time() - start_time
        if num_samples is not(None):
            total_samples = sum(num_samples.values())
            results = results.append({'m' : total_samples, 'eps' : prc_grid[prc], 'time' : total_time, 'algo' : 'psp', 'type' : 'hoeffding'}, ignore_index = True)

# Save results to .csv file
results.to_csv('results/progressive_data_num_players_' + str(num_players) + '_num_actions_' + str(num_actions) + '_' + util_random.id_generator() + '.csv')