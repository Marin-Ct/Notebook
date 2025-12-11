"""Main script to run the alien classification workflow.

This program demonstrates the core tasks of the lab in a single run:

1. Read a JSON input file and display the raw content.
2. Parse the JSON into Python data structures and print the parsed result.
3. Convert the parsed data into Alien objects and display them.
4. Perform simple filtering on the aliens (e.g., find even IDs) for practice.
5. Classify the aliens by universe.
6. Write the classification result back to a JSON file.

The script aims to be easy to understand and modify.  It requires a file
named ``input.json`` to exist in the same directory.  A sample
``input.json`` is provided with the project.
"""

from __future__ import annotations

from typing import List

from .alien import Alien
from .reader import JsonReader
from .classifier import Classifier
from .view import View


def main() -> None:
    """Run the full lab workflow in sequence."""
    # Determine the path to the input and output files relative to this script.
    import os
    package_dir = os.path.dirname(__file__)
    input_filename = os.path.join(package_dir, "input.json")
    output_filename = os.path.join(package_dir, "output.json")

    # Day 2: Read and print the raw and parsed JSON file
    reader = JsonReader(input_filename)
    try:
        raw_text = reader.read_text()
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found. Make sure it is present in the project folder.")
        return
    print("Raw JSON contents:\n", raw_text, sep="")

    data = reader.parse_json()
    print("\nParsed JSON data:")
    print(data)

    # Day 3: Map JSON objects to instances of Alien
    aliens: List[Alien] = []
    for item in data:
        # Extract values with sensible defaults if keys are missing
        alien_id = item.get("id")
        name = item.get("name", "Unknown")
        species = item.get("species", "Unknown")
        universe = item.get("universe", "Unknown")
        # Only create an Alien if id is present and convertible to int
        try:
            alien_id_int = int(alien_id)
        except (TypeError, ValueError):
            print(f"Warning: Skipping entry with invalid id: {alien_id}")
            continue
        aliens.append(Alien(alien_id_int, name, species, universe))

    # Print the list of Alien objects
    print("\nAlien objects:")
    for alien in aliens:
        print(" ", alien)

    # Example filtering: find aliens with even IDs
    even_id_aliens = [alien for alien in aliens if alien.id % 2 == 0]
    print("\nAliens with even IDs:", [alien.id for alien in even_id_aliens])

    # Day 4: Classification by universe
    classifier = Classifier(aliens)
    groups = classifier.classify_by_universe()
    print("\nAliens grouped by universe:")
    for universe, group in groups.items():
        print(f" {universe}: {[alien.name for alien in group]}")

    # Day 5: Save the grouped result to a JSON output file
    View.save_groups_to_json(groups, output_filename)
    print(f"\nClassification written to '{output_filename}'.")


if __name__ == "__main__":
    main()
