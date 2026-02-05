"""CSC111 Project 1: Text Adventure Game - Interact

===============================
This Python module contains the code for player interactions/actions based on location

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any
from game_entities import Location

class Interact:
    """Desc.

    Pre-conditions? RI's?
    Instance Attributes:
    - loc_id: id of location
    - interactables: list of available interaceables at a location
    """
    location: Location
    interactables: list[str]


    def trade(self, give_item: Optional[Any] = None, recieve_item: Optional[Any] = None):
        """Desc.
        
        """
    
    def puzzle(self, ):
        """Desc.
        """
    