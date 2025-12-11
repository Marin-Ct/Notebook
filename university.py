from typing import List, Optional

from .faculty import Faculty


class University:
    """Represents the Technical University with multiple faculties.

    This class maintains a list of faculties and provides helper methods
    to create faculties, search for a faculty by student identifier and
    display information about faculties.  It does not persist any data
    between sessions; all information lives in memory for the duration of
    the program run.
    """

    def __init__(self) -> None:
        self.faculties: List[Faculty] = []

    def create_faculty(self, name: str, field: str) -> Faculty:
        """Create a new faculty and register it with the university."""
        faculty = Faculty(name, field)
        self.faculties.append(faculty)
        return faculty

    def find_faculty_of_student(self, student_id: str) -> Optional[Faculty]:
        """Return the faculty where the student with the given id is enrolled or graduated.

        Searches through all faculties to find a match.  If found, returns
        the Faculty instance; otherwise returns ``None``.
        """
        for faculty in self.faculties:
            # Check current students and graduates within the faculty
            if faculty.find_student(student_id) is not None:
                return faculty
        return None

    def find_faculty_by_name(self, name: str) -> Optional[Faculty]:
        """Return a faculty by its name (case insensitive).

        If no faculty with the given name exists, returns ``None``.
        """
        for faculty in self.faculties:
            if faculty.name.lower() == name.lower():
                return faculty
        return None

    def faculties_by_field(self, field: str) -> List[Faculty]:
        """Return a list of faculties matching the given field (case insensitive)."""
        return [faculty for faculty in self.faculties if faculty.field.lower() == field.lower()]
