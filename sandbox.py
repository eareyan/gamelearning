#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 16:48:08 2018

@author: enriqueareyan

    This file is just to play around with code.

    TODO:
        1) things are implemented with old Cyru's formula, should implement new formula
"""
from rademacher import Rademacher
from brg import BRG
import test_games
import util_random

prisonersDilemma = test_games.get_prisonersDilemma()
testGame = test_games.get_testGame()
game3Players = test_games.get_game3Players()


(eps, conf) = Rademacher.compute_confidence_intervals(prisonersDilemma.get_noisy_samples(2000), 2000, 0.01)
sample_individual_BRGS = BRG.construct_all_estimated_eps_individual_restricted_brgs(prisonersDilemma, conf)
BRG.plot_graph(sample_individual_BRGS[0])
BRG.plot_graph(sample_individual_BRGS[1])
sample_BRG = BRG.get_estimated_eps_brg(prisonersDilemma, conf)
BRG.plot_graph(sample_BRG)

(eps, conf) = Rademacher.compute_confidence_intervals(testGame.get_noisy_samples(2000), 2000, 0.1)
sample_individual_BRGS = BRG.construct_all_estimated_eps_individual_restricted_brgs(testGame, conf)
BRG.plot_graph(sample_individual_BRGS[0])
BRG.plot_graph(sample_individual_BRGS[1])
sample_BRG = BRG.get_estimated_eps_brg(testGame, conf)
BRG.plot_graph(sample_BRG)

(eps, conf) = Rademacher.compute_confidence_intervals(game3Players.get_noisy_samples(2000), 2000, 0.1)
sample_individual_BRGS = BRG.construct_all_estimated_eps_individual_restricted_brgs(game3Players, conf)
BRG.plot_graph(sample_individual_BRGS[0])
BRG.plot_graph(sample_individual_BRGS[1])
BRG.plot_graph(sample_individual_BRGS[2])
sample_BRG = BRG.get_estimated_eps_brg(game3Players, conf)
BRG.plot_graph(sample_BRG)

# Random Game

random_game = util_random.generate_random_game(3,3)

(eps, conf) = Rademacher.compute_confidence_intervals(random_game.get_noisy_samples(2000), 2000, 0.1)
sample_individual_BRGS = BRG.construct_all_estimated_eps_individual_restricted_brgs(random_game, conf)
BRG.plot_graph(sample_individual_BRGS[0])
BRG.plot_graph(sample_individual_BRGS[1])
BRG.plot_graph(sample_individual_BRGS[2])
sample_BRG = BRG.get_estimated_eps_brg(random_game, conf)
BRG.plot_graph(sample_BRG)


#TODO: To graph the graph! run the following. Still need to find out how to color edges.
#from networkx.drawing.nx_pydot import write_dot
#write_dot(sample_BRG, 'test1.dot')
# Run the following in terminal
#neato -T png test1.dot > test1.png
