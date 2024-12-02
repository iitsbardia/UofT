class Player:
    """A Player

        Attributes:
        - name: name of the player.
        - history: history of the player scores this games

        Sample Usage:

        Creating a player:
        >>> p = Player('Bardiya')
        >>> p.name
        'Bardiya'
        >>> p.add_score(10)
        >>> p.add_score(20)
        >>> p.add_score(21)
        >>> p.add_score(21)
        >>> p.add_score(19)
        >>> p.history
        [10,20,21,21,19]
        >>> p.highscore()
        21
        >>> p.average()
        18.2
        """

    name: str
    history: list[int]

    def __init__(self, name: str) -> None:
        """Initialize a new Player."""

        self.name = name
        self.history = []

    def __str__(self) -> str:
        """Return a string representation of the Player."""
        return (f"PLayer {self.name},"
                f" average {self.average()}, highscore: {self.highscore()}")

    def add_score(self, score: int) -> None:
        self.history.append(score)

    def highscore(self) -> int:
        if not self.history:
            return 0
        return max(self.history)

    def average(self) -> float:
        if not self.history:
            return 0.0
        lst = self.history
        return sum(lst) / len(lst)


if __name__ == '__main__':
    import random
    p = Player('Bardiya')
    for i in range(5):
        score = random.randint(0,100)
        p.add_score(score)

    print(p)
