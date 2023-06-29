#!/usr/bin/env python3

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
