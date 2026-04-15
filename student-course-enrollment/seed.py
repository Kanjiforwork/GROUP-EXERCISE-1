from pathlib import Path

from src.data.database import DATABASE_PATH, initialize_database
from src.services.enrollment_service import EnrollmentService


def main() -> None:
    database_path = Path(DATABASE_PATH)
    if database_path.exists():
        database_path.unlink()

    initialize_database(database_path)
    service = EnrollmentService(database_path)

    alice = service.create_student("Alice Nguyen", "alice@example.com")
    bob = service.create_student("Bob Tran", "bob@example.com")

    python_course = service.create_course("CS101", "Introduction to Python", 3)
    database_course = service.create_course("DB201", "Database Fundamentals", 4)

    service.enroll_student(alice.id, python_course.id)
    service.enroll_student(alice.id, database_course.id)
    bob_enrollment = service.enroll_student(bob.id, python_course.id)
    service.update_grade(bob_enrollment.id, "A")

    print(f"Seeded database at {database_path}")
    print("Sample students, courses, and enrollments were created successfully.")


if __name__ == "__main__":
    main()
