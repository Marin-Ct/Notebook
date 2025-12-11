class Student:
    """Represents a university student with a unique identifier and a name.

    This class is kept deliberately simple.  Each student has an `id` used
    to identify them across the university and a `name` for human‑friendly
    output.  The attributes are public for ease of access in this
    introductory assignment.
    """

    def __init__(self, student_id: str, name: str) -> None:
        """Create a new Student.

        Args:
            student_id: A unique identifier for the student (for example an email
                address or a numeric ID).
            name: The full name of the student.
        """
        self.id = student_id
        self.name = name

    def __str__(self) -> str:
        """Return a human‑readable representation of the student."""
        return f"{self.name} ({self.id})"
