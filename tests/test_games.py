#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 09:41:01 2018

@author: eareyanv
    A few games to test.
"""
from structures import game, player


def get_prisonersDilemma():
    # Construct standard prisoners' Dilemma game
    playerPD = player.Player(2)
    payoff = {(0, 0, 0): -1,
              (0, 0, 1): -1,
              (0, 1, 0): -3,
              (0, 1, 1): 0,
              (1, 0, 0): 0,
              (1, 0, 1): -3,
              (1, 1, 0): -2,
              (1, 1, 1): -2}
    prisonersDilemma = game.Game("Prisoner's Dilemma", [playerPD, playerPD], payoff)
    # print(prisonersDilemma)
    return prisonersDilemma


def get_testGame():
    # A game with different number of actions per player
    playerA = player.Player(2)
    playerB = player.Player(3)
    payoff = {(0, 0, 0): 1,
              (0, 0, 1): 1,
              (0, 1, 0): 1,
              (0, 1, 1): 1,
              (0, 2, 0): 2,
              (0, 2, 1): 2,
              (1, 0, 0): 2,
              (1, 0, 1): 2,
              (1, 1, 0): 3,
              (1, 1, 1): 3,
              (1, 2, 0): 3,
              (1, 2, 1): 12}
    testGame = game.Game('Just a test game', [playerA, playerB], payoff)
    # print(testGame)
    return testGame


def get_game2Players():
    # A different test
    playerTwoActions = player.Player(2)
    payoff = {(0, 0, 0): 10,
              (0, 0, 1): 10,
              (0, 1, 0): 10,
              (0, 1, 1): 10,
              (1, 0, 0): 10,
              (1, 0, 1): 10,
              (1, 1, 0): 0,
              (1, 1, 1): 0}
    game2Players = game.Game('Game to test without randomness', [playerTwoActions, playerTwoActions], payoff)
    # print(game2Players)
    return game2Players


def get_game3Players():
    # Game with 3 players
    player_three_actions = player.Player(3)
    payoff = {(0, 0, 0, 0): 10,
              (0, 0, 0, 1): 10,
              (0, 0, 0, 2): 10,
              (1, 0, 0, 0): 10,
              (1, 0, 0, 1): 10,
              (1, 0, 0, 2): 10,
              (0, 1, 0, 0): 10,
              (0, 1, 0, 1): 10,
              (0, 1, 0, 2): 10,
              (0, 0, 1, 0): 10,
              (0, 0, 1, 1): 10,
              (0, 0, 1, 2): 10,
              (1, 1, 0, 0): 10,
              (1, 1, 0, 1): 10,
              (1, 1, 0, 2): 10,
              (1, 0, 1, 0): 10,
              (1, 0, 1, 1): 10,
              (1, 0, 1, 2): 10,
              (0, 1, 1, 0): 10,
              (0, 1, 1, 1): 10,
              (0, 1, 1, 2): 10,
              (1, 1, 1, 0): 10,
              (1, 1, 1, 1): 10,
              (1, 1, 1, 2): 10}
    game3Players = game.Game('Game with 3 players', [player_three_actions, player_three_actions, player_three_actions], payoff)
    # print(game3Players)
    return game3Players


def get_epsNashGame():
    player_2Actions = player.Player(2)

    payoffs = {(0, 0, 0): -3.9339330570746132,
               (1, 0, 0): 0.58271604875483263,
               (0, 0, 1): -4.3383564301842164,
               (0, 1, 1): -3.4820535274941156,
               (0, 1, 0): -4.8676012765600998,
               (1, 1, 0): 2.917255869939873,
               (1, 0, 1): 4.6817979956722429,
               (1, 1, 1): 4.3807981344515916}

    game2Players = game.Game('Game with 2 players to test eps-Nash', [player_2Actions, player_2Actions], payoffs)
    return game2Players
