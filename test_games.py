#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 09:41:01 2018

@author: eareyanv
    A few games to test.
"""
from game import Game
from player import Player

def get_prisonersDilemma():
    # Construct standard prisoners' Dilemma game
    player = Player(2)
    payoff = {(0,0,0) : -1,
              (0,0,1) : -1,
              (0,1,0) : -3,
              (0,1,1) : 0,
              (1,0,0) : 0,
              (1,0,1) : -3,
              (1,1,0) : -2,
              (1,1,1) : -2}
    prisonersDilemma = Game("Prisoner's Dilemma", [player, player], payoff)
    #print(prisonersDilemma)
    return prisonersDilemma

def get_testGame():
    # A game with different number of actions per player
    playerA = Player(2)
    playerB = Player(3)
    payoff = {(0,0,0) : 1,
              (0,0,1) : 1,
              (0,1,0) : 1,
              (0,1,1) : 1,
              (0,2,0) : 2,
              (0,2,1) : 2,
              (1,0,0) : 2,
              (1,0,1) : 2,
              (1,1,0) : 3,
              (1,1,1) : 3,
              (1,2,0) : 3,
              (1,2,1) : 12}
    testGame = Game('Just a test game', [playerA, playerB], payoff)
    print(testGame)
    return testGame

def get_game2Players():
    # A different test
    playerTwoActions = Player(2)
    payoff = {(0,0,0) : 10,
              (0,0,1) : 10,
              (0,1,0) : 10,
              (0,1,1) : 10,
              (1,0,0) : 10,
              (1,0,1) : 10,
              (1,1,0) : 0,
              (1,1,1) : 0}
    game2Players = Game('Game to test without randomness', [playerTwoActions, playerTwoActions], payoff)
    print(game2Players)
    return game2Players

def get_game3Players():
    # Game with 3 players
    playerTwoActions = Player(2)
    payoff = {(0,0,0,0) : 10,
              (0,0,0,1) : 10,
              (0,0,0,2) : 10,
              (1,0,0,0) : 10,
              (1,0,0,1) : 10,
              (1,0,0,2) : 10,
              (0,1,0,0) : 10,
              (0,1,0,1) : 10,
              (0,1,0,2) : 10,
              (0,0,1,0) : 10,
              (0,0,1,1) : 10,
              (0,0,1,2) : 10,
              (1,1,0,0) : 10,
              (1,1,0,1) : 10,
              (1,1,0,2) : 10,
              (1,0,1,0) : 10,
              (1,0,1,1) : 10,
              (1,0,1,2) : 10,
              (0,1,1,0) : 10,
              (0,1,1,1) : 10,
              (0,1,1,2) : 10,
              (1,1,1,0) : 10,
              (1,1,1,1) : 10,
              (1,1,1,2) : 10}
    game3Players = Game('Game with 3 players', [playerTwoActions, playerTwoActions, playerTwoActions], payoff)
    print(game3Players)
    return game3Players
