#!/usr/bin/env python3
# Kyler Farnsworth
# KFarnsworth1@csu.fullerton.edu
# @Tabushabu

"""
Imports the the game demo and executes the main function.
"""

import sys
from videogame import game

if __name__ == "__main__":
    # TODO: Prepare and run the game
    game = game.Game()
    game.run_game()
    sys.exit(0)
