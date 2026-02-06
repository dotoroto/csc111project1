"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Any


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: A unique non-negative integer identifying this location.
        - name: The name of the location shown to the player.
        - descriptions:
            index 0: The name of the location shown to the player.
            index 1: A short description displayed after the location has
            already been visited.
            index 2: A detailed description displayed the first time the
            player enters the location or when the 'look' command is used.
            index 3: A description displayed after the location’s
            main interaction has been completed.
        - available_commands: A mapping from direction strings ('north', 'south',
            'east', 'west') to location id numbers indicating where the player
            moves when using a 'go' command.
        - items: A list of item names currently present at this location.
        - enter_requirement: A condition that must be satisfied for the player
            to enter this location (e.g., possessing a specific item), or an
            empty string if there is no requirement.
        - interaction: A list of interactions or actions that can occur at this
            location.
        - visited: Whether the player has visited this location before.
        - action_completed: Whether the location’s main interaction or puzzle
            has been completed.

    Representation Invariants:
        - id_num >= 0
        - available_commands maps valid direction strings to valid location IDs
        - visited and action_completed are boolean values
        - items contains only item names (strings)
        - enter_requirement is either an empty string or a valid item name
    """
    id_num: int
    descriptions: list[str]
    available_commands: dict[str, int]
    items: list[str]
    enter_requirement: str
    interaction: list[Any]
    visited: bool = False
    action_completed: bool = False


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item.
        - description: A description of the item shown to the player.
        - target_points: The number of points awarded when the item is correctly
            used or deposited at its target location.
        - weight: The weight of the item, used to limit how many items the player
            can carry.

    Representation Invariants:
        - name != ''
        - target_points >= 0
        - weight >= 0
    """
    name: str
    description: str
    target_points: int
    weight: float


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    #import python_ta
    #python_ta.check_all(config={
    #    'max-line-length': 120,
    #    'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    #})
