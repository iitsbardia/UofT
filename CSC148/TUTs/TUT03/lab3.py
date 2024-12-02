"""CSC148 Lab 3: Inheritance

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the implementation of a simple number game.
The key class design feature here is *inheritance*, which is used to enable
different types of players, both human and computer, for the game.
"""
from __future__ import annotations
import random

from python_ta.contracts import check_contracts


################################################################################
# Below is the implementation of NumberGame.
#
# You do not have to modify this class, but you should read through it and
# understand how it uses the Player class (and its subclasses) that you'll
# be implementing.
#
# As you read through, make note of any methods or attributes a Player will
# need.
################################################################################
@check_contracts
class NumberGame:
    """A number game for two players.

    A count starts at 0. On a player's turn, they add to the count an amount
    between a set minimum and a set maximum. The player who brings the count
    to a set goal amount is the winner.

    The game can have multiple rounds.

    Attributes:
    - goal:
        The amount to reach in order to win the game.
    - min_step:
        The minimum legal move.
    - max_step:
        The maximum legal move.
    - current:
        The current value of the game count.
    - players:
        The two players.
    - turn:
        The turn the game is on, beginning with turn 0.
        If turn is even number, it is players[0]'s turn.
        If turn is any odd number, it is player[1]'s turn.

    Representation Invariants:
    - self.turn >= 0
    - 0 <= self.current <= self.goal
    - 0 < self.min_step <= self.max_step <= self.goal
    """
    goal: int
    min_step: int
    max_step: int
    current: int
    players: tuple[Player, Player]
    turn: int

    def __init__(self, goal: int, min_step: int, max_step: int,
                 players: tuple[Player, Player]) -> None:
        """Initialize this NumberGame.

        Preconditions:
        - 0 < min_step <= max_step <= goal
        """
        self.goal = goal
        self.min_step = min_step
        self.max_step = max_step
        self.current = 0
        self.players = players
        self.turn = 0

    def play(self) -> str:
        """Play one round of this NumberGame. Return the name of the winner.

        A "round" is one full run of the game, from when the count starts
        at 0 until the goal is reached.
        """
        while self.current < self.goal:
            self.play_one_turn()
        # The player whose turn would be next (if the game weren't over) is
        # the loser. The one who went one turn before that is the winner.
        loser = self.whose_turn(self.turn)
        winner = self.whose_turn(self.turn - 1)
        winner.record_win()
        loser.record_loss()
        return winner.name

    def whose_turn(self, turn: int) -> Player:
        """Return the Player whose turn it is on the given turn number.
        """
        if turn % 2 == 0:
            return self.players[0]
        else:
            return self.players[1]

    def play_one_turn(self) -> None:
        """Play a single turn in this NumberGame.

        Determine whose move it is, get their move, and update the current
        total as well as the number of the turn we are on.
        Print the move and the new total.
        """
        next_player = self.whose_turn(self.turn)
        amount = next_player.move(
            self.current,
            self.min_step,
            self.max_step,
            self.goal
        )
        self.current += amount

        # We set a hard limit on self.current
        # (This is a strange corner case: don't worry about it!)
        if self.current > self.goal:
            self.current = self.goal

        self.turn += 1

        print(f'{next_player.name} moves {amount}.')
        print(f'Total is now {self.current}.')


################################################################################
# Implement your Player class and it subclasses below!
################################################################################


class Player:
    """A number game player.

    ***Abstract Class, should not be instantiated.***

    This class serves as a base for different types of players in the number game.
    Subclasses must implement the move method to define how the player will make a move.

    Attributes:
        name (str): The name of the player.
        wins (int): The number of wins the player has.
        losses (int): The number of losses the player has.
    """

    name: str
    wins: int
    losses: int

    def __init__(self, name: str) -> None:
        """Initialize this player.

        Args:
            name (str): The name of the player.
        """
        self.name = name
        self.wins = 0
        self.losses = 0

    def move(self, current: int, min_: int, max_: int, goal: int) -> int:
        """Abstract method that must be implemented by subclasses.

        This method defines how a player makes a move by selecting a number to add
        to the current count. Subclasses should implement this method to provide
        the specific strategy for the player.

        Args:
            current (int): The current count in the game.
            min_ (int): The minimum number a player can add to the count.
            max_ (int): The maximum number a player can add to the count.
            goal (int): The goal count that players aim to reach or exceed to win.

        Returns:
            int: The number added to the count.
        """
        raise NotImplementedError

    def record_win(self) -> None:
        """Records a win.

        Increments the player's win count by 1.
        """
        self.wins += 1

    def record_loss(self) -> None:
        """Records a loss.

        Increments the player's loss count by 1.
        """
        self.losses += 1


class RandomPlayer(Player):
    """A player that makes random moves within the allowed range.

    This player selects a random number between the minimum and maximum values
    on each turn, without any strategic consideration.
    """

    def __init__(self, name: str) -> None:
        """Initialize this player.

        Args:
            name (str): The name of the player.
        """
        super().__init__(name)

    def move(self, current: int, min_: int, max_: int, goal: int) -> int:
        """Make a random move.

        Selects a random integer between the minimum and maximum values.

        Args:
            current (int): The current count in the game.
            min_ (int): The minimum number a player can add to the count.
            max_ (int): The maximum number a player can add to the count.
            goal (int): The goal count that players aim to reach or exceed to win.

        Returns:
            int: A randomly selected number between min_ and max_.
        """
        return random.randint(min_, max_)


class UserPlayer(Player):
    """A player controlled by the user.

    This player makes moves based on user input, allowing direct interaction.
    """

    def __init__(self, name: str) -> None:
        """Initialize this player.

        Args:
            name (str): The name of the player.
        """
        super().__init__(name)

    def move(self, current: int, min_: int, max_: int, goal: int) -> int:
        """Prompt the user to enter a move.

        Requests the user to input a number within the specified range.

        Args:
            current (int): The current count in the game.
            min_ (int): The minimum number a player can add to the count.
            max_ (int): The maximum number a player can add to the count.
            goal (int): The goal count that players aim to reach or exceed to win.

        Returns:
            int: The number entered by the user.
        """
        return int(input(f'Enter a move between {min_} and {max_}: ').strip())


class StrategicPlayer(Player):
    """A strategic player that attempts to make the optimal move.

    This player aims to make moves that leave the opponent in a losing position,
    increasing the chances of winning by strategic calculation.
    """

    def __init__(self, name: str) -> None:
        """Initialize this player.

        Args:
            name (str): The name of the player.
        """
        super().__init__(name)

    def move(self, current: int, min_: int, max_: int, goal: int) -> int:
        """Make the optimal move to leave the opponent in a losing position.

        This method calculates the best move to make based on the current count,
        aiming to leave the opponent with fewer winning options.

        Args:
            current (int): The current count in the game.
            min_ (int): The minimum number a player can add to the count.
            max_ (int): The maximum number a player can add to the count.
            goal (int): The goal count that players aim to reach or exceed to win.

        Returns:
            int: The best number to add to the count to maintain an advantage.
        """
        for i in range(max_, min_ - 1, -1):
            if (current + i) % (max_ + min_ + 1) == 0:
                return i
        return max_


@check_contracts
def make_player(generic_name: str) -> Player:
    """Return a new Player based on user input.

    Allow the user to choose a player name and player type.
    <generic_name> is a placeholder used to identify which player is being made.

    If the inputted name starts with an "s", make a StrategicPlayer.
    If the inputted name starts with a "u", make a UserPlayer.
    Otherwise, make a RandomPlayer.
    """
    name = input(f'Enter a name for {generic_name}: ')
    if name[0] == "u" or name[0] == "U":
        return UserPlayer(name)
    elif name[0] == "s" or name[0] == "S":
        return StrategicPlayer(name)
    else:
        return RandomPlayer(name)


################################################################################
# The main game program
################################################################################


def main() -> None:
    """Play multiple rounds of a NumberGame based on user input settings.
    """
    goal = int(input('Enter goal amount: '))
    minimum = int(input('Enter minimum move: '))
    maximum = int(input('Enter maximum move: '))
    p1 = make_player('p1')
    p2 = make_player('p2')
    while True:
        g = NumberGame(goal, minimum, maximum, (p1, p2))
        winner = g.play()
        print(f'And {winner} is the winner!!!')
        print(p1)
        print(p2)
        again = input('Again? (y/n) ')
        if again != 'y':
            return


if __name__ == '__main__':
    # Uncomment the following line to run the number game.
    main()

    # Uncomment to check your work with python_ta!
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['random'],
    #     'allowed-io': [
    #         'main',
    #         'make_player',
    #         'UserPlayer.move',
    #         'NumberGame.play_one_turn'
    #     ],
    #     'max-line-length': 100
    # })
