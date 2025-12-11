"""Defines a simple View class for writing classification results to JSON files.

The View class converts groups of Alien objects (produced by the
Classifier) into a JSON‑serialisable structure and writes it to a
file.  Using this class separates the presentation/output logic from
the core classification logic.
"""

import json
from typing import Dict, List

from .alien import Alien


class View:
    """Provides utilities for outputting classification results."""

    @staticmethod
    def save_groups_to_json(groups: Dict[str, List[Alien]], filename: str) -> None:
        """Save the classified aliens to a JSON file.

        Args:
            groups: Mapping from universe names to lists of Alien objects.
            filename: The name of the output file.
        """
        # Convert Alien objects into dictionaries suitable for JSON dumping
        output = {}
        for universe, aliens in groups.items():
            output[universe] = [
                {
                    "id": alien.id,
                    "name": alien.name,
                    "species": alien.species,
                    "universe": alien.universe,
                }
                for alien in aliens
            ]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
