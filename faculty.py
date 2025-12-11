from typing import List, Optional

from .student import Student


class Faculty:
    """Represents a faculty within the university.

    A faculty has a name and a field (for example "Computer Science" or
    "Food Technology").  It keeps track of currently enrolled students and
    those who have graduated.  All operations that modify the lists of
    students are simple list operations; this lab assignment does not require
    optimised data structures.
    """

    def __init__(self, name: str, field: str) -> None:
        """Create a new faculty with a given name and field."""
        self.name = name
        self.field = field
        self.current_students: List[Student] = []
        self.graduated_students: List[Student] = []

    def add_student(self, student: Student) -> None:
        """Enroll a student into this faculty.

        The student is appended to the list of currently enrolled students.
        Duplicate identifiers are not checked here; it is the caller's
        responsibility to ensure a student is not enrolled twice.
        """
        self.current_students.append(student)

    def graduate_student(self, student_id: str) -> bool:
        """Graduate the student with the provided identifier.

        If the student is currently enrolled, they are moved from the
        `current_students` list to the `graduated_students` list and the
        method returns ``True``.  If no matching student is found, the
        method returns ``False``.
        """
        for index, student in enumerate(self.current_students):
            if student.id == student_id:
                self.graduated_students.append(student)
                # Remove from current students
                del self.current_students[index]
                return True
        return False

    def has_student(self, student_id: str) -> bool:
        """Check if a student with the given identifier is currently enrolled."""
        return any(student.id == student_id for student in self.current_students)

    def find_student(self, student_id: str) -> Optional[Student]:
        """Find a student by identifier in both current and graduated lists.

        Returns the Student object if found, otherwise ``None``.  This helper
        can be used by the University class when searching for students.
        """
        for student in self.current_students:
            if student.id == student_id:
                return student
        for student in self.graduated_students:
            if student.id == student_id:
                return student
        return None
