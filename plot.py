#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 08:26:03 2018

@author: enriqueareyan
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import matplotlib


font = {'family' : 'normal',
        'size'   : 12}

matplotlib.rc('font', **font)

def plot_num_failures(ps_data, psp_data):
    """ Plot num failures of an algorithm """
    ps_data['counter'] = 1
    ps_data = ps_data.groupby('eps').sum()
    index = np.arange(len(ps_data.index))

    psp_data['counter'] = 1
    psp_data = psp_data.groupby('eps').sum()
    
    ax = plt.subplot(111)    
    ax.bar(index + 0.2, ps_data['counter'].values, width=0.4)
    ax.bar(index + 0.5, psp_data['counter'].values, width=0.4, color = 'r')

    plt.xticks(index, ps_data.index.values)
    plt.title('Number of successful runs')
    plt.xlabel('Error tolerance, $\epsilon$')

def save_sample_plot(num_players, num_actions, ps_rademacher_plot_data, psp_rademacher_plot_data, ps_hoeffding_plot_data, psp_hoeffding_plot_data, title_post_fix, caption):
    """ Plot m (data complexity) """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_yscale('log')
    plt.plot(ps_rademacher_plot_data['m'], label = 'Progressive Sampling (rademacher)')
    plt.plot(psp_rademacher_plot_data['m'], label = ' Progressive Sampling with Prunning (rademacher)')
    plt.plot(ps_hoeffding_plot_data['m'], label = 'Progressive Sampling (hoeffding)')
    plt.plot(psp_hoeffding_plot_data['m'], label = ' Progressive Sampling with Prunning (hoeffding)')
    plt.legend()
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    plt.title('Sample complexity \n ' + title_post_fix)
    plt.xlabel('Error tolerance, $\epsilon$')
    plt.ylabel('Number of samples')
    fig.text(0, -.1, caption, ha='left')
    fig.set_size_inches(8, 5)
    fig.savefig('plots/sample_' + str(num_players) + '_players_' + str(num_actions) + '_actions.png', bbox_inches='tight')
    plt.show()

def save_time_plot(num_players, num_actions, ps_rademacher_plot_data, psp_rademacher_plot_data, ps_hoeffding_plot_data, psp_hoeffding_plot_data, title_post_fix, caption):
    """ Plot time complexity """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_yscale('log')
    plt.plot(ps_rademacher_plot_data['time'], label = 'Progressive Sampling (rademacher)')
    plt.plot(psp_rademacher_plot_data['time'], label = ' Progressive Sampling with Prunning (rademacher)')
    plt.plot(ps_hoeffding_plot_data['time'], label = 'Progressive Sampling (hoeffding)')
    plt.plot(psp_hoeffding_plot_data['time'], label = ' Progressive Sampling with Prunning (hoeffding)')
    plt.legend()
    plt.title('Time complexity \n ' + title_post_fix)
    plt.xlabel('Error tolerance, $\epsilon$')
    plt.ylabel('Time (s)')
    fig.text(0, -.2, caption, ha='left')
    fig.set_size_inches(8, 5)    
    plt.show()
    fig.savefig('plots/time_' + str(num_players) + '_players_' + str(num_actions) + '_actions.png', bbox_inches='tight')
    


results_dict = {'QY6V82': (2, 2),
                'X8EAEG': (2, 3), 
                'IDQNX7': (2, 4), 
                'ES7N6O': (3, 2),
                'HMC1SF': (3, 3),
                'WCRQZ4': (3, 4),
                'M0DZOA': (4, 2),
                'MM0KZ6': (4, 3),
                'K1UMF0': (5, 2)}

for (game_id, (num_players, num_actions)) in results_dict.items():
    results = pd.read_csv('results/progressive_data_num_players_' + str(num_players) + '_num_actions_' + str(num_actions) + '_' + game_id + '.csv')
    
    m = 100
    max_num_samples = 100000
    caption = 'Parameters: \n  Failure probability $\delta = 0.1$, \n  Initial number of samples is ' + str(m) + ' \n  Maximum number of samples is ' + "{:,}".format(max_num_samples)
    # The size of the game is (num_actions^num_players) * num_players
    title_post_fix = 'Random game with ' + str(num_players) + ' players, each with '+str(num_actions) + ' actions, game size: ' + str((num_actions ** num_players) * num_players)
    
    # Prepare data for plots.
    ps_rademacher_data = results[(results['algo'] == 'ps') & (results['type'] == 'rademacher')]    
    psp_rademacher_data = results[(results['algo'] == 'psp') & (results['type'] == 'rademacher')]    
    ps_rademacher_data['m'] = ps_rademacher_data['m'].astype(int)
    psp_rademacher_data['m'] = psp_rademacher_data['m'].astype(int)

    ps_hoeffding_data = results[(results['algo'] == 'ps') & (results['type'] == 'hoeffding')]    
    psp_hoeffding_data = results[(results['algo'] == 'psp') & (results['type'] == 'hoeffding')]    
    ps_hoeffding_data['m'] = ps_hoeffding_data['m'].astype(int)
    psp_hoeffding_data['m'] = psp_hoeffding_data['m'].astype(int)
    
    # Group data for epsilon
    ps_rademacher_plot_data = ps_rademacher_data.groupby('eps').mean()
    psp_rademacher_plot_data = psp_rademacher_data.groupby('eps').mean()

    ps_hoeffding_plot_data = ps_hoeffding_data.groupby('eps').mean()
    psp_hoeffding_plot_data = psp_hoeffding_data.groupby('eps').mean()
    
    # Plot
    save_sample_plot(num_players, num_actions, ps_rademacher_plot_data, psp_rademacher_plot_data, ps_hoeffding_plot_data, psp_hoeffding_plot_data, title_post_fix, caption)
    save_time_plot(num_players, num_actions, ps_rademacher_plot_data, psp_rademacher_plot_data, ps_hoeffding_plot_data, psp_hoeffding_plot_data, title_post_fix, caption)
 