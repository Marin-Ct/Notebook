"""Defines the Alien class for the alien classification lab.

This simple data class stores information about an alien species: a unique
identifier, a name, a species (the race or type of alien), and the
universe the alien belongs to.  It provides a human‑readable
representation for debugging or printing purposes.
"""


class Alien:
    """Represents a single alien entity.

    Attributes:
        id (int): Unique identifier for the alien (e.g., numeric ID).
        name (str): Name of the alien.
        species (str): The species or race of the alien.
        universe (str): The fictional universe the alien belongs to.
    """

    def __init__(self, alien_id: int, name: str, species: str, universe: str) -> None:
        self.id = alien_id
        self.name = name
        self.species = species
        self.universe = universe

    def __repr__(self) -> str:
        """Return a detailed string representation of the alien."""
        return (
            f"Alien(id={self.id}, name='{self.name}', species='{self.species}', "
            f"universe='{self.universe}')"
        )
