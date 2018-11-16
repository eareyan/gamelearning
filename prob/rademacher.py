#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:01:15 2018

@author: eareyanv
    A class centralizing all operations involving Rademacher complexity, including computation of confidence intervals.
"""
import numpy as np
import math


class Rademacher:

    @staticmethod
    def sample_rade_vars(m):
        """
            Compute a vector of m Rademacher variables, i.e., variables that
            are -1 with probability 1/2 and 1 with probability 1/2.
            """
        return [1 if np.random.uniform(0, 1) >= 0.5 else -1 for i in range(0, m)]

    @staticmethod
    def one_draw_emp_rc(samples, rade_vars, m):
        """
            Compute the 1-Draw Empirical Rademacher Complexity
        """
        if len(rade_vars) != m:
            raise Exception(
                'The lenght of the rademacher vector should be ' + str(m) + ' but is ' + str(len(rade_vars)))
        avg_utilities = []
        for (strategy_profile_player, utility_sample) in samples.items():
            number_of_samples = len(utility_sample)
            if number_of_samples != m:
                raise Exception('The number of samples for profile ' + str(strategy_profile_player) + ' is ' + str(
                    number_of_samples) + ' but should be ' + str(m))
            # At some point we tested this weird expression.
            # avg_utilities.append(max(0.0, sum(i[0] * (i[1] - 0.5) for i in zip(rade_vars, utility_sample)) / number_of_samples))
            avg_utilities.append(sum(i[0] * i[1] for i in zip(rade_vars, utility_sample)) / number_of_samples)
        return max(avg_utilities)

    @staticmethod
    def compute_confidence_intervals(samples, m, delta, hoeffding_inequality=False, size_of_family=-1, discount_factor=1.0):
        """
            Given a set of m samples and delta, compute the confidence interval
            for each strategy profile and player.
        """
        if hoeffding_inequality:
            if size_of_family < 0:
                raise Exception('Size of family must be a positive integer')
            # For experimental purposes, I have set c = 1 here.
            # print("Computing H for:", m, delta, size_of_family)
            # eta = math.sqrt((math.log((2.0 * size_of_family) / delta)) / (2.0 * m))
            eta = math.sqrt(-1.0 * math.log(1.0 - (1.0 - delta) ** (1.0 / size_of_family)) / (2 * m))
            radius = eta
        else:
            # For experimental purposes, I have set c = 1 here.
            eta = 3.0 * math.sqrt((math.log(2.0 / delta)) / (2.0 * m))
            # We might me able to tight the bound, but its seems difficult:
            # eta = 2.0 * math.sqrt((math.log(1.0 / delta)) / (2.0 * m))
            r = Rademacher.one_draw_emp_rc(samples, Rademacher.sample_rade_vars(m), m)
            radius = 2.0 * r + eta
        eps = discount_factor * (2.0 * radius)
        average_util = {}
        conf_util = {}
        for (strategy_profile_player, utility_sample) in samples.items():
            average_util[strategy_profile_player] = sum(u for u in utility_sample) / m
            conf_util[strategy_profile_player] = (
            average_util[strategy_profile_player] - radius, average_util[strategy_profile_player] + radius)
        return eps, conf_util
