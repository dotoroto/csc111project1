"""CSC111 Project 1: Text Adventure Game - Interact

===============================
This Python module contains the code for player interactions/actions based on location

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any
from game_entities import Location
import random

class Interact:
    """Description:
    An (abstract) class containing methods for all possible interactions with all items in the game

    Pre-conditions? RI's?
    Instance Attributes:
    - loc_id: id of location
    - interactables: list of available items that you can interact with at a location
    """
    location: Location
    interactables: Optional[list[str]] = None


    def trade(self, give_item: Optional[Any] = None, recieve_item: Optional[Any] = None):
        """Desc.
        
        """

    
    def puzzle(self):
        """Desc.
        """
        #Generate a random list of 3 numbers that represent the locker combination
        combination = [random.randint(0, 40) for x in range(0,3)]

        #Change to hexadecimal
        cmi = []

    