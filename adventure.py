"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from event_logger import Event, EventList



# Note: You may add in other import statements here as needed
import random

# Note: You may add helper functions, classes, etc. below as needed
LOCK_CODE = random.randint(1000, 9999)
CRYPIC_MESSAGE = hex(LOCK_CODE)

class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the id representing the player's current location
        - ongoing: ? # TODO

    Representation Invariants:
        - current_location_id >= 1
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_inv: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    score: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.score = 0
        self.current_inv = []

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'], loc_data['available_commands'], loc_data['items'],
                                    loc_data['enter_requirement'], loc_data['interaction'])
            locations[loc_data['id']] = location_obj

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        # YOUR CODE BELOW
        for item_data in data['items']:  # Go through each element associated with the 'locations' key in the file
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        # YOUR CODE BELOW
        if loc_id is None:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]

    def get_item(self, item_name: str) -> Item | None:
        """Return Item object associated with the provided object name."""
        for item in self._items:
            if item.name == item_name:
                return item
        return None

    def display_inv(self):
        """Prints the current items that the user has in their inventory and the description of each item"""
        if len(self.current_inv):
            print("Your current inventory is empty.")
            return
        for item in self.current_inv:
            print("-", item.name)

    def trade(self, given_location: Location) -> None:
        """Check if user has item required for trade at given location.
        If they do, complete the trade and print what has happened."""
        give_items = given_location.interaction[0]
        recieve_item = given_location.interaction[1]

        all_give_items_exist = all([self.get_item(item) in self.current_inv for item in give_items])
        if all_give_items_exist:
            for item in give_items:
                self.current_inv.remove(self.get_item(item))
            for item in recieve_item:
                self.current_inv.append(self.get_item(item))
                print("You now have", item, "in your inventory")
            given_location.available_commands.pop("trade")
        else:
            print("You do not have the required items to complete this action.")

    def interact(self, given_location: Location) -> None:
        """Give user items from the interaction at a specified location."""
        recieve_item = given_location.interaction
        for item in recieve_item:
            self.current_inv.append(self.get_item(item))
            print("You now have", item, "in your inventory")
        given_location.available_commands.pop("interact")

    def submit(self, given_location) -> None:
        """If possible, user submits projects and wins if they completed the requirements.
        Otherwise, tell them they can't submit yet."""
        give_items = given_location.interaction[0]

        all_give_items_exist = all([self.get_item(item) in self.current_inv for item in give_items])
        if all_give_items_exist:
            print("Congratulations, you submitted your project on time! You cheer and celebrate.",
                  "Hopefully you get an 100%!")
            self.ongoing = False
        else:
            print("You do not have the required items to submit your project yet.")

if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE
        game_log.add_event(Event(location.id_num, location.long_description, None, None, game_log.last), choice)

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        print("You are at", location.name)
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("================")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            if choice == "log":
                game_log.display_events()
            elif choice == "look":
                print(location.long_description)
            elif choice == "inventory":
                print("Your current inventory:")
                game.display_inv()
            elif choice == "score":
                print("Your current score is:", game.score)
            elif choice == "quit":
                print("You have quit the game.")
                game.ongoing = False
        # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)

        else:
            # Handle non-menu actions
            result = location.available_commands[choice]

            if choice.startswith("go "):
                key_needed = game.get_location(result).enter_requirement
                if key_needed == '':
                    game.current_location_id = result
                else:
                    if game.get_item(key_needed) in game.current_inv:
                        print("You use your", key_needed, "and go in.")
                        game.current_location_id = result
                    else:
                        print("You need a", key_needed, "to enter.")
            else:
                if choice == "search":
                    if len(location.items) > 0:
                        grabbable_item = game.get_item(location.items[0])
                        game.current_inv.append(grabbable_item)
                        print(grabbable_item.description)
                        print("You pick up the " + location.items[0] + ".")
                        location.items.pop(0)

                        if len(location.items) == 0:
                            location.available_commands.pop("search")
                    else:
                        print("You search around the area but find nothing.")

                elif choice == "trade":
                    game.trade(location)

                elif choice == "interact":
                    game.interact(location)

                elif choice == "submit choice":
                    game.submit(location)
        print("================")
