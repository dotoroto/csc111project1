"""CSC111 Project 1: Text Adventure Game - Interact

===============================
This Python module contains the code for player interactions/actions based on location

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any
from game_entities import Location, Item
from adventure import AdventureGame


class Interact:
    """Desc.

    Pre-conditions? RI's?
    Instance Attributes:
    - loc_id: id of location
    - interactables: list of available interaceables at a location
    """
    location: Location

    def trade(self, game: AdventureGame) -> None:
        """Check if user has item. If they do, complete the trade and print what has happened."""
        give_item = None
        recieve_item = None

        #check location to figure out items to give and recieve
        if self.location.name == "Robarts Commons":
            recieve_item = game.get_item("lucky mug")

        if give_item is None:
            #item is given away for free
            game.current_inv.append(recieve_item)
            print("You now have", recieve_item.name, "in your inventory")
            self.location.available_commands.pop("interact")
        elif give_item in game.current_inv:
            #check if trade item is in user inventory
            game.current_inv.remove(give_item)
            game.current_inv.append(recieve_item)
            print("You now have", recieve_item.name, "in your inventory")
            self.location.available_commands.pop("interact")
        else:
            print("You do not have the required items to complete this action.")

    def puzzle(self, ):
        """Desc.
        """
