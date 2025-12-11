"""Contains functionality to group Alien objects by their universe.

The Classifier class takes a sequence of Alien instances and provides
a method to classify them into groups based on their universe.  Each
group is represented as a dictionary mapping universe names to lists
of Alien objects.  This grouping can then be output or otherwise
processed by a View class.
"""

from typing import Dict, List

from .alien import Alien


class Classifier:
    """Classifies aliens by their universe.

    This class accepts a list of Alien objects and provides a method to
    group them by universe.  The classification result is a dictionary
    mapping each unique universe string to a list of Alien objects from
    that universe.
    """

    def __init__(self, aliens: List[Alien]) -> None:
        self.aliens = aliens

    def classify_by_universe(self) -> Dict[str, List[Alien]]:
        """Group aliens by their universe.

        Returns:
            Dict[str, List[Alien]]: A mapping from universe names to lists of
                Alien instances belonging to that universe.
        """
        groups: Dict[str, List[Alien]] = {}
        for alien in self.aliens:
            groups.setdefault(alien.universe, []).append(alien)
        return groups
