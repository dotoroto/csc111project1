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
    MAX_WEIGHT: int = 1100

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
        self.current_inv = [self.get_item("tcard")]

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
            location_obj.available_commands["search"] = -1
            locations[loc_data['id']] = location_obj

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        # YOUR CODE BELOW
        for item_data in data['items']:  # Go through each element associated with the 'locations' key in the file
            item_obj = Item(item_data['name'], item_data['description'], item_data['target_points']
                            , item_data['weight'])
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

    def interact_inv(self):
        """Prints the current items that the user has in their inventory and the description of each item"""
        if len(self.current_inv) == 0:
            print("Your current inventory is empty.")
            return
        for item in self.current_inv:
            print("-", item.name, " : ", item.weight, "g", sep="")

        print("Total weight: ", sum([item.weight for item in self.current_inv]), "/", self.MAX_WEIGHT, sep="")

        specific_item = input("\nInput object to select, or 'nothing': ").strip().lower()
        if specific_item == 'nothing':
            return

        if self.get_item(specific_item) not in self.current_inv:
            print("That was not a valid object.")
            return

        print("You can inspect or drop or neither")
        action = input("What action would you like to perform: ").strip().lower()

        if action == "inspect":
            print(self.get_item(specific_item).description)
            print(specific_item, "weighs", self.get_item(specific_item).weight)
            if specific_item == 'cipher message item':
                print("It seems to have some writing:", cryptic_message)
        elif action == "drop":
            self._locations[self.current_location_id].items.append(specific_item)
            self.current_inv.remove(self.get_item(specific_item))
        elif action == "neither":
            return
        else:
            print("That was not a valid option.")

    def search(self, loc: Location) -> None:
        """Displays items at given location, and prompts if user wants to pick it up"""
        if len(loc.items) > 0:
            print("You find the following:")
            for item in loc.items:
                print(item + " - weighs ", self.get_item(item).weight,"g", sep="")

            pickup = input("\nInput object to pickup, or 'nothing': ").strip().lower()
            if pickup in loc.items:
                current_weight = sum([i.weight for i in self.current_inv])
                if current_weight + self.get_item(pickup).weight > self.MAX_WEIGHT:
                    print("You can't pick this item up. You're already carrying too much... "
                          "Drop something and try again")
                else:
                    self.current_inv.append(self.get_item(pickup))
                    loc.items.remove(pickup)
            else:
                print("That was not an available item.")

        else:
            print("You find nothing :(")

    def display_map(self) -> None:
        """Display ASCII map of game"""
        print("+---+---+---+---+----+")
        print("| 1 | 2 | 8 | 9 | 10 |")
        print("+---+---+---+---+----+")
        print("    | 3 |       | 11 |")
        print("    +---+       +----+")
        print("    | 4 |       | 12 |")
        print("+---+---+---+   +----+")
        print("| 6 | 5 | 7 |")
        print("+---+---+---+")

    def trade(self, loc: Location) -> bool:
        """Check if user has item required for trade at given location.
        If they do, complete the trade and print what has happened."""
        given_items = loc.interaction[0]
        recieve_item = loc.interaction[1]

        all_give_items_exist = all([self.get_item(item) in self.current_inv for item in given_items])
        if all_give_items_exist:
            for item in given_items:
                self.current_inv.remove(self.get_item(item))
            for item in recieve_item:
                self.current_inv.append(self.get_item(item))
                print("You now have", item, "in your inventory")
                self.score += self.get_item(item).target_points
            loc.available_commands.pop("trade")
            return True
        else:
            print("You do not have the required items to complete this action.")
            return False

    def interact(self, loc: Location) -> None:
        """Give user items from the interaction at a specified location."""
        recieve_item = loc.interaction
        for item in recieve_item:
            self.current_inv.append(self.get_item(item))
            self.score += self.get_item(item).target_points
            print("You now have", item, "in your inventory")
        if "interact" in loc.available_commands:
            loc.available_commands.pop("interact")

    def submit(self, loc) -> None:
        """If possible, user submits projects and wins if they completed the requirements.
        Otherwise, tell them they can't submit yet."""
        give_items = loc.interaction[0]
        all_give_items_exist = all([self.get_item(item) in self.current_inv for item in give_items])
        if all_give_items_exist:
            print("Congratulations, you submitted your project on time! You cheer and celebrate.",
                  "Hopefully you get an 100%! Your score is:", self.score)
            self.ongoing = False
        else:
            print("You do not have the required items to submit your project yet.")

    def puzzle(self) -> bool:
        """
        Prompts the user to enter the 3-digit locker combination to unlock the locker

        Note: The 3 digits come from the crypti message which is in hexadecimal
        """
        user_answer = []
        print("Huh, you need 3 numbers to unlock it...where could you get this? (please reword)")
        suffixes = ["1st", "2nd", "3rd"]
        for combo in range(3):
            print(suffixes[combo] + " digit: ")
            user_answer.append(int(input()))

        return user_answer == combination


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
    menu = ["look", "inventory", "map", "score", "log", "quit"]  # Regular menu options available at each location
    choice = None
    moves = 0

    # We generate a new cryptic message (an item used in the game) every time the game is ran
    # Generate a random list of 3 numbers that represent the locker combination
    combination = []
    for i in range(0, 3):
        num = random.randint(10, 15)
        # while loop handles repetitive numbers as opposed to a comprehension
        while num in combination:
            num = random.randint(10, 15)

        combination.append(num)
    # Change to hexadecimal
    cryptic_message = [hex(num).upper() for num in combination]

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing and moves < 45:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE
        game_log.add_event(Event(location.id_num, location.long_description), choice)

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        print(location.id_num, "You are at", location.name)
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, map, score, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("\n================\n")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            if choice == "log":
                game_log.display_events()
            elif choice == "look":
                print(location.long_description)
            elif choice == "inventory":
                print("Your current inventory:")
                game.interact_inv()
            elif choice == "map":
                game.display_map()
            elif choice == "score":
                print("Your current score is:", game.score)
            elif choice == "quit":
                print("You have quit the game.")
                game.ongoing = False

        else:
            # Handle non-menu actions
            result = location.available_commands[choice]

            if choice.startswith("go "):
                key_needed = game.get_location(result).enter_requirement
                if key_needed == '':
                    game.current_location_id = result
                    moves += 1
                else:
                    if game.get_item(key_needed) in game.current_inv:
                        print("You use your", key_needed, "and go in.")
                        game.current_location_id = result
                        moves += 1
                    else:
                        print("You need a", key_needed, "to enter.")
            else:
                if choice == "search":
                    game.search(location)
                elif choice == "trade":
                    game.trade(location)
                elif choice == "ask lost and found":
                    game.interact(location)
                elif choice == "submit project":
                    game.submit(location)
                elif choice == "open locker":
                    if game.puzzle():
                        print("The lock opens!")
                        game.interact(location)
                    else:
                        print("The combination was incorrect.")
                elif choice == "grab USB":
                    if game.trade(location):
                        print("Yay! Your USB is now in your inventory")
                    else:
                        print("You try to grab it with your bare hands, but it won't reach.",
                              "You realize a ruler and some chewed up gum might help...")

        print("\n================\n")

    if moves >= 45:
        print("You have exceeded the maximum amount of moves.",
              "You were running around too much and ran out of time.",
              "Unfortunately, you recieved a 0 on your project.",
              "Better luck next time.")

"""
to-dos
- make score real
- clean up code
"""
