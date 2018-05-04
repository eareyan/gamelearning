#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:01:15 2018

@author: eareyanv
    A class centralizing all operations involving Rademacher complexity, including 
    computation of confidence intervals.
"""
import numpy as np
import math
from util_random import noise_c

class Rademacher:
    
    @staticmethod
    def sample_rade_vars(m):
        """
            Compute a vector of m Rademacher variables, i.e., variables that
            are -1 with probability 1/2 and 1 with probability 1/2.
            """
        return [1 if np.random.uniform(0, 1) >= 0.5 else -1 for i in range(0,m)]
    
    @staticmethod
    def one_draw_emp_rc(samples, rade_vars, m):
        """
            Compute the 1-Draw Empirical Rademacher Complexity
        """
        if(len(rade_vars) != m):
            raise Exception('The lenght of the rademacher vector should be ' 
                            + str(m) + ' but is ' + str(len(rade_vars)))
        avg_utilities = []
        for (strat_profile_player, utility_sample) in samples.items():
            number_of_samples = len(utility_sample)
            if(number_of_samples != m):
                raise Exception('The number of samples for profile ' 
                                + str(strat_profile_player) + ' is ' + str(number_of_samples)
                                + ' but should be ' + str(m))
            #avg_utilities.append(max(0.0, sum(i[0] * (i[1] - 0.5) for i in zip(rade_vars, utility_sample)) / number_of_samples))
            avg_utilities.append(sum(i[0] * (i[1] - 0.5) for i in zip(rade_vars, utility_sample)) / number_of_samples)
        return max(avg_utilities)
    
    @staticmethod
    def compute_confidence_intervals(samples, m, delta):
        """
            Given a set of m samples and delta, compute the confidence interval
            for each strategy profile and player.
        """
        eta =  3.0 * noise_c * math.sqrt((math.log(2.0 / delta)) / (2.0 * m))
        #eta =  3 * math.sqrt((math.log(2 / delta)) / (2 * m))
        r   = Rademacher.one_draw_emp_rc(samples, Rademacher.sample_rade_vars(m), m)
        eps = 2*(2*r + eta)
        #print('eta = ', eta)
        #print('r = ', r)
        #print('eps = ' , eps)
        aveg_util = {}
        conf_util = {}
        for (strat_profile_player, utility_sample) in samples.items():
            aveg_util[strat_profile_player] = sum(u for u in utility_sample) / m
            conf_util[strat_profile_player] = (aveg_util[strat_profile_player] - 2*r - eta, aveg_util[strat_profile_player] + 2*r + eta)
        return (eps, conf_util)