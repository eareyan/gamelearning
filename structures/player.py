#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:54:52 2018

@author: eareyanv
"""


class Player:
    """A player of a normal-form game. 
    
    Attributes:
        numActions  Actions are normalized to be between 0 and numActions
    """
    numActions = None

    def __init__(self, numActions):
        self.numActions = numActions

    def __str__(self):
        return "Player with " + str(self.numActions) + " actions: " + ', '.join(
            str(a) for a in range(0, self.numActions))
