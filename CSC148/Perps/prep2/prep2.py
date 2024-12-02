"""CSC148 Prep 2: Object Oriented Programming

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Diane Horton, and Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 David Liu, Diane Horton, and Sophia Huynh

=== Module Description ===
This module contains the documentation for a simple class. Your job is to
implement the class below according to its docstring; note this includes
both the *instance attributes* of the class and the *methods* we've documented.

As usual, delete the

There is also a task inside prep2_starter_tests.py.
Make sure to look at that file and complete the
"""
# Do NOT use any imports beyond these (randint and date)!
from random import randint
from datetime import date
from python_ta.contracts import check_contracts


################################################################################
# Part 1
# In this part of the prep, you will be implementing a Spinner class.
# A 'Spinner' refers to the type of spinner used in games.
#
# For example, consider the following spinner with 4 slots:
#           0
#           ^
#      3    |     1
#
#           2
# Initially, the spinner arrow's position (represented by the line |) is at 0.
#
# If we spin and force it to move forward 1 spot, then it'll look
# like this:
#           0
#
#      3     ----> 1
#
#           2
# And the spinner arrow's position is now at 1.
# If we force it to move another 2 spaces, then it'll look like this:
#           0
#
#      3 <----     1
#
#           2
# Where the spinner arrow's position is at 3.
################################################################################
@check_contracts
class Spinner:
    """A spinner for a board game.

    A spinner has a certain number of slots, numbered starting at 0 and
    increasing by 1 each slot. For example, if the spinner has 6 slots,
    they are numbered 0 through 5, inclusive.

    A spinner also has an arrow that points to one of these slots.

    Attributes:
    - slots:
        The number of slots in this spinner.
    - position:
        The slot number that the spinner's arrow is currently pointing to.

    Sample Usage:

    Creating a spinner:
    >>> s = Spinner(8)
    >>> s.position
    0

    Spinning the spinner:
    >>> s.spin(4)
    >>> s.position
    4
    >>> s.spin(2)
    >>> s.position
    6
    >>> s.spin(2)
    >>> s.position
    0
    """
    slots: int
    position: int

    def __init__(self, size: int) -> None:
        """Initialize a new spinner with <size> slots.

        A spinner's position always starts at 0.

        Precondition: size >= 1
        """
        self.slots = size
        self.position = 0

    def spin(self, force: int) -> None:
        """Spin this spinner, advancing the arrow <force> slots.

        The spinner wraps around once it reaches its maximum slot, starting
        back at 0. See the class docstring for an example of this.

        Precondition: force >= 0

        Hint: use the "%" operator to "wrap around" the spinner's position.
              The "%" operator gets the 'remainder'.
              For example, 8 % 6 == 2
        """
        force = force % self.slots
        self.position += force
        self.position = self.position % self.slots

    def spin_randomly(self) -> None:
        """Spin this spinner randomly.

        This modifies the spinner's arrow to point to a random slot on the
        spinner. Each slot has an equal chance of being pointed to.

        You MUST use randint (imported from random) for this method, to
        choose a random slot. Check out the official Python documentation:
        https://docs.python.org/3/library/random.html#random.randint
        """
        slot = randint(0, self.slots - 1)
        self.position = slot


################################################################################
# Part 2
# In this part of the prep, you will be working with the Tweet class from the
# reading for this prep: 3.1 Introduction to Object-Oriented Programming
################################################################################
@check_contracts
class Tweet:
    """A tweet, like in Twitter.

    Attributes:
        userid: the id of the user who wrote the tweet.
        created_at: the date the tweet was written.
        content: the contents of the tweet.
        likes: the number of likes this tweet has received.

    Representation Invariants:
        - len(self.content) <= 280
    """
    # Attribute types
    userid: str
    created_at: date
    content: str
    likes: int

    def __init__(self, who: str, when: date, what: str) -> None:
        """Initialize a new Tweet."""
        self.userid = who
        self.created_at = when
        self.content = what
        self.likes = 0

    def like(self, n: int) -> None:
        """Add <n> likes to <self>'s likes.

        Adds a specified number of likes to the tweet's current number of likes.

        Preconditions:
        - n > 0

        >>> tweet = Tweet('Sophia', date(2021, 1, 1), 'Happy new year!')
        >>> tweet.likes
        0
        >>> tweet.like(3)
        >>> tweet.likes
        3
        >>> tweet.like(2)
        >>> tweet.likes
        5
        """
        self.likes += n

    def unlike(self) -> None:
        """Remove 1 like from <self>'s likes.
         Precondition: self.likes > 0

         >>> tweet = Tweet('Sophia', date(2021, 1, 1), 'Happy new year!')
         >>> tweet.like(5)
         >>> tweet.likes
         5
         >>> tweet.unlike()
         >>> tweet.likes
         4
         """
        if self.likes > 0:
            self.likes -= 1


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run prep2" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['random', 'datetime'],
        'max-line-length': 100
    })
