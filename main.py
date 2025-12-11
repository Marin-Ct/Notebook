"""Simple interactive Student Management system for grade 6 assignment.

This program provides a command line interface for managing faculties and
students at a fictitious university.  It intentionally omits complex
features such as persistence to disk or detailed logging in order to
remain accessible for beginners.  The focus is on practicing object
oriented design: classes represent students, faculties and the
university as a whole, and the main loop orchestrates user requests.

Usage:
    python main.py

The program will display a main menu from which the user can perform
general operations or manage individual faculties.  The session runs
until the user selects the ``exit`` option from the main menu.
"""

from __future__ import annotations

from typing import Optional

from .student import Student
from .university import University


def prompt_nonempty(prompt: str) -> str:
    """Prompt the user until a non‑empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def manage_faculty(faculty) -> None:
    """Display and handle the faculty operations menu for a single faculty."""
    while True:
        print(f"\nManaging faculty: {faculty.name} (Field: {faculty.field})")
        print("Faculty Operations:")
        print(" 1. Enroll a student")
        print(" 2. Graduate a student")
        print(" 3. Display current students")
        print(" 4. Display graduates")
        print(" 5. Check if a student belongs to this faculty")
        print(" 0. Back to main menu")
        choice = input("Select an option: ").strip()
        if choice == "1":
            # Enroll a student
            student_id = prompt_nonempty("Enter student ID: ")
            name = prompt_nonempty("Enter student name: ")
            # Do not check for duplicate IDs at this basic level; duplicates
            # may occur if the user enters the same ID twice.
            student = Student(student_id, name)
            faculty.add_student(student)
            print(f"Student {student} enrolled successfully.")
        elif choice == "2":
            # Graduate a student
            student_id = prompt_nonempty("Enter student ID to graduate: ")
            if faculty.graduate_student(student_id):
                print(f"Student {student_id} has been graduated.")
            else:
                print(f"No currently enrolled student with ID {student_id} found.")
        elif choice == "3":
            # Display current students
            if faculty.current_students:
                print("Current students:")
                for student in faculty.current_students:
                    print(f" - {student}")
            else:
                print("No students are currently enrolled in this faculty.")
        elif choice == "4":
            # Display graduates
            if faculty.graduated_students:
                print("Graduated students:")
                for student in faculty.graduated_students:
                    print(f" - {student}")
            else:
                print("No graduates yet for this faculty.")
        elif choice == "5":
            # Check membership of a student
            student_id = prompt_nonempty("Enter student ID to check: ")
            if faculty.has_student(student_id):
                print(f"Student {student_id} is currently enrolled in this faculty.")
            else:
                # Check graduates as well for completeness
                if any(s.id == student_id for s in faculty.graduated_students):
                    print(f"Student {student_id} has graduated from this faculty.")
                else:
                    print(f"Student {student_id} does not belong to this faculty.")
        elif choice == "0":
            # Return to the main menu
            break
        else:
            print("Invalid option. Please try again.")


def main() -> None:
    """Run the main program loop for managing the university."""
    university = University()
    print("Welcome to the Student Management System!\n")
    while True:
        print("Main Menu:")
        print(" 1. Create a new faculty")
        print(" 2. Find the faculty of a student (by ID)")
        print(" 3. Display all faculties")
        print(" 4. Display faculties by field")
        print(" 5. Manage a specific faculty")
        print(" 0. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            # Create a new faculty
            name = prompt_nonempty("Enter faculty name: ")
            field = prompt_nonempty("Enter faculty field: ")
            university.create_faculty(name, field)
            print(f"Faculty '{name}' with field '{field}' created successfully.\n")
        elif choice == "2":
            # Find faculty by student ID
            student_id = prompt_nonempty("Enter student ID: ")
            faculty = university.find_faculty_of_student(student_id)
            if faculty:
                print(f"Student {student_id} belongs to faculty: {faculty.name} (Field: {faculty.field}).\n")
            else:
                print(f"Student {student_id} does not belong to any faculty.\n")
        elif choice == "3":
            # Display all faculties
            if not university.faculties:
                print("No faculties have been created yet.\n")
            else:
                print("University Faculties:")
                for fac in university.faculties:
                    print(f" - {fac.name} (Field: {fac.field})")
                print()
        elif choice == "4":
            # Display faculties by field
            field = prompt_nonempty("Enter field to filter by: ")
            matching = university.faculties_by_field(field)
            if matching:
                print(f"Faculties with field '{field}':")
                for fac in matching:
                    print(f" - {fac.name}")
                print()
            else:
                print(f"No faculties found with field '{field}'.\n")
        elif choice == "5":
            # Manage a specific faculty
            if not university.faculties:
                print("No faculties exist yet. Create one first.\n")
                continue
            name = prompt_nonempty("Enter the name of the faculty to manage: ")
            faculty = university.find_faculty_by_name(name)
            if faculty:
                manage_faculty(faculty)
            else:
                print(f"Faculty '{name}' not found.\n")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Allow graceful exit on Ctrl+C
        print("\nExiting. Goodbye!")
