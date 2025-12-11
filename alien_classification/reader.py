"""Provides a simple utility for reading and parsing JSON files.

The JsonReader class encapsulates reading raw file contents and
parsing a JSON file into Python data structures.  This class does
minimal error handling for simplicity; in a production system,
additional checks would be appropriate.  Using this class helps
encapsulate file I/O and JSON parsing from the rest of the program.
"""

import json
from typing import Any, List


class JsonReader:
    """Utility for reading text and JSON from a file."""

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read_text(self) -> str:
        """Read the entire file as a raw string.

        Returns:
            str: The raw contents of the file.
        """
        with open(self.filename, "r", encoding="utf-8") as f:
            return f.read()

    def parse_json(self) -> Any:
        """Parse the JSON file and return the resulting Python object.

        Returns:
            Any: The parsed JSON data (often a dict or list).
        """
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)
