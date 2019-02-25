#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 16:48:08 2018

@author: enriqueareyan

    This file is just to play around with code.
"""
from structures import brg, game
from prob import rademacher, util_random
from tests import test_games
from congestion import congestion_game_lib
import numpy as np

congestion_game = congestion_game_lib.simpleCongestionGame1()
print("congestion_game_1 = ", congestion_game)
print("True pure eq = ", congestion_game.get_pure_eps_nash())
print("PPOA = ", congestion_game.get_pure_price_of_anarchy())

# congestion_game = congestion_game_lib.simpleCongestionGame2()
# print("congestion_game_2 = ", congestion_game)
# print("PPOA = ", congestion_game.get_pure_price_of_anarchy())


num_samples = 10000
noise_function = f = lambda: np.random.uniform(0.0, 1.0)
noise_function = f = lambda: np.random.uniform(-1.0, 0.0)
noise_function = f = lambda: np.random.uniform(-0.5, 0.5)
samples = congestion_game.get_noisy_samples(num_samples, noise_function)
delta = 0.1
eps, means = rademacher.Rademacher.compute_confidence_intervals(samples=samples,
                                                                m=num_samples,
                                                                delta=delta,
                                                                hoeffding_inequality=True,
                                                                size_of_family=congestion_game.get_size_of_game(),
                                                                return_only_means=True)
estimated_game = game.Game("estimated Game", congestion_game.listOfPlayers, means)
print("estimated_game = ", estimated_game)
print("eps = ", eps)
print("2eps Pure Nash = ", estimated_game.get_pure_eps_nash(eps))
print("estimated \eps PPOA = ", estimated_game.get_pure_price_of_anarchy(eps))

exit()

prisonersDilemma = test_games.get_prisonersDilemma()
testGame = test_games.get_testGame()
game3Players = test_games.get_game3Players()

(eps, conf) = rademacher.Rademacher.compute_confidence_intervals(prisonersDilemma.get_noisy_samples(2000), 2000, 0.01)
sample_individual_BRGS = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(prisonersDilemma, conf)
brg.BRG.plot_graph(sample_individual_BRGS[0])
brg.BRG.plot_graph(sample_individual_BRGS[1])
sample_BRG = brg.BRG.get_estimated_eps_brg(prisonersDilemma, conf)
brg.BRG.plot_graph(sample_BRG)

(eps, conf) = rademacher.Rademacher.compute_confidence_intervals(testGame.get_noisy_samples(2000), 2000, 0.1)
sample_individual_BRGS = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(testGame, conf)
brg.BRG.plot_graph(sample_individual_BRGS[0])
brg.BRG.plot_graph(sample_individual_BRGS[1])
sample_BRG = brg.BRG.get_estimated_eps_brg(testGame, conf)
brg.BRG.plot_graph(sample_BRG)

(eps, conf) = rademacher.Rademacher.compute_confidence_intervals(game3Players.get_noisy_samples(2000), 2000, 0.1)
sample_individual_BRGS = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(game3Players, conf)
brg.BRG.plot_graph(sample_individual_BRGS[0])
brg.BRG.plot_graph(sample_individual_BRGS[1])
brg.BRG.plot_graph(sample_individual_BRGS[2])
sample_BRG = brg.BRG.get_estimated_eps_brg(game3Players, conf)
brg.BRG.plot_graph(sample_BRG)

# Random Game

random_game = util_random.generate_random_game(3, 3)

(eps, conf) = rademacher.Rademacher.compute_confidence_intervals(random_game.get_noisy_samples(2000), 2000, 0.1)
sample_individual_BRGS = brg.BRG.construct_all_estimated_eps_individual_restricted_brgs(random_game, conf)
brg.BRG.plot_graph(sample_individual_BRGS[0])
brg.BRG.plot_graph(sample_individual_BRGS[1])
brg.BRG.plot_graph(sample_individual_BRGS[2])
sample_BRG = brg.BRG.get_estimated_eps_brg(random_game, conf)
brg.BRG.plot_graph(sample_BRG)

# TODO: To graph the graph! run the following. Still need to find out how to color edges.
# from networkx.drawing.nx_pydot import write_dot
# write_dot(sample_BRG, 'test1.dot')
# Run the following in terminal
# neato -T png test1.dot > test1.png
