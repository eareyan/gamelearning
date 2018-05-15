#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:42:26 2018

@author: enriqueareyan
"""
import util_random
import psp
import sampling
import time
import pandas as pd
#import argparse

#parser = argparse.ArgumentParser(description='Run experiments')
#parser.add_argument("numplayers", "numactions", required=True)
#parser.parse_args()

# Generate a random game.
num_players = 4
num_actions = 2
experiment_game = util_random.generate_random_game(num_players, num_actions, False)
# Test these percentages
prc_grid =[0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]

delta = 0.1
m = 100
max_num_samples = 100000
results = pd.DataFrame(columns = ['m','eps','time', 'algo'])

ps_fails = {}
psp_fails = {}
for prc in range(0, 10):
    ps_fails[prc] = 0
    psp_fails[prc] = 0
    for t in range(0, 100):
        eps = abs(experiment_game.get_max_payoff() * prc_grid[prc]) 
        print('Run #', t, ' \t ', prc_grid[prc], ' \t eps = ', eps)
        
        # First run progressive sampling
        start_time = time.time()
        (num_samples, eps_hat, delta_hat, conf, dict_individual_estimated_eps_brgs) = sampling.progressive_sampling(experiment_game, eps, delta, m, max_num_samples, False)
        if num_samples is None:
            ps_fails[prc] = ps_fails[prc] + 1
        else:
            total_samples = num_samples * len(experiment_game.payoffs)
            total_time = time.time() - start_time
            results = results.append({'m': total_samples, 'eps': prc_grid[prc], 'time': total_time, 'algo':'ps'}, ignore_index = True)
        
        # Second run psp
        start_time = time.time()
        (num_samples, eps_hat, delta_hat, conf, dict_individual_estimated_eps_brgs) = psp.psp(experiment_game, eps, delta, m, max_num_samples, False)
        if num_samples is None:
            psp_fails[prc] = psp_fails[prc] + 1
        else:
            total_samples = sum(num_samples.values())
            total_time = time.time() - start_time
            results = results.append({'m': total_samples, 'eps': prc_grid[prc], 'time': total_time, 'algo':'psp'}, ignore_index = True)

# Save results to .csv file
results.to_csv('results/progressive_data_num_players_' + str(num_players) + '_num_actions_' + str(num_actions) + '_' + util_random.id_generator() + '.csv')