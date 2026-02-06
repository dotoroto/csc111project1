"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

You can copy/paste your code from Assignment 1 into this file, and modify it as
needed to work with your game.

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
from dataclasses import dataclass
from typing import Optional


# TODO: Copy/paste your A1 event_logger code below, and modify it if needed to fit your game


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - id_num: Integer id of this event's location
    - description: Long description of this event's location
    - next_command: String command which leads this event to the next event, None if this is the last game event
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    """
    id_num: int
    description: str
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: The first game event in the event list
        - last: The last game event in the event list

    Representation Invariants:
        - (self.first is None) == (self.last is None)
        - not(self.first is not None) or self.first.prev is None
        - not(self.last is not None) or self.last.next is None
    """
    first: Optional[Event]
    last: Optional[Event]

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.first = None
        self.last = None

    def display_events(self) -> None:
        """Display all events in chronological order."""
        curr = self.first
        while curr.next:
            print(f"Location: {curr.id_num}, Command: {curr.next_command}")
            curr = curr.next

    # TODO: Complete the methods below, based on the given descriptions.
    def is_empty(self) -> bool:
        """Return whether this event list is empty."""

        # TODO: Your code below
        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """
        Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        # Hint: You should update the previous node's <next_command> as needed

        # TODO: Your code below
        if self.is_empty():
            self.first = event

        else:
            # Based on representation invariants, I can assume that
            # last != None because if self.is_empty() then self.first is None so self.last is None
            self.last.next = event
            self.last.next_command = command
            event.prev = self.last
        self.last = event

    def remove_last_event(self) -> None:
        """
        Remove the last event from this event list.
        If the list is empty, do nothing.
        """
        # Hint: The <next_command> and <next> attributes for the new last event should be updated as needed

        # TODO: Your code below
        if self.is_empty():
            return

        if self.first == self.last:
            self.first = None
            self.last = None

        else:
            self.last = self.last.prev
            self.last.next = None
            self.last.next_command = None

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""

        # TODO: Your code below
        curr = self.first
        id_log = []
        while curr is not None:
            id_log.append(curr.id_num)
            curr = curr.next
        return id_log


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })
