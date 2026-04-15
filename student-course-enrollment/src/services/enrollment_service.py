from pathlib import Path
from sqlite3 import IntegrityError

from src.data.database import DATABASE_PATH, initialize_database
from src.domain.entities import Course, Enrollment, Student
from src.repositories.course_repository import CourseRepository
from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.student_repository import StudentRepository


class EnrollmentService:
    def __init__(self, database_path: str | Path = DATABASE_PATH) -> None:
        self.database_path = Path(database_path)
        initialize_database(self.database_path)
        self.student_repository = StudentRepository(self.database_path)
        self.course_repository = CourseRepository(self.database_path)
        self.enrollment_repository = EnrollmentRepository(self.database_path)

    def create_student(self, name: str, email: str) -> Student:
        clean_name = name.strip()
        clean_email = email.strip()

        if not clean_name:
            raise ValueError("Student name cannot be empty.")
        if not clean_email:
            raise ValueError("Student email cannot be empty.")

        try:
            return self.student_repository.create(clean_name, clean_email)
        except IntegrityError as exc:
            raise ValueError("Student email already exists.") from exc

    def create_course(self, code: str, title: str, credits: int) -> Course:
        clean_code = code.strip().upper()
        clean_title = title.strip()

        if not clean_code:
            raise ValueError("Course code cannot be empty.")
        if not clean_title:
            raise ValueError("Course title cannot be empty.")
        if credits <= 0:
            raise ValueError("Course credits must be greater than zero.")

        try:
            return self.course_repository.create(clean_code, clean_title, credits)
        except IntegrityError as exc:
            raise ValueError("Course code already exists.") from exc

    def enroll_student(self, student_id: int, course_id: int) -> Enrollment:
        student = self.student_repository.get_by_id(student_id)
        if student is None:
            raise ValueError(f"Student with id {student_id} does not exist.")

        course = self.course_repository.get_by_id(course_id)
        if course is None:
            raise ValueError(f"Course with id {course_id} does not exist.")

        try:
            return self.enrollment_repository.enroll(student_id, course_id)
        except IntegrityError as exc:
            raise ValueError("Student is already enrolled in this course.") from exc

    def update_grade(self, enrollment_id: int, grade: str) -> Enrollment:
        clean_grade = grade.strip().upper()
        if not clean_grade:
            raise ValueError("Grade cannot be empty.")

        enrollment = self.enrollment_repository.get_by_id(enrollment_id)
        if enrollment is None:
            raise ValueError(f"Enrollment with id {enrollment_id} does not exist.")

        self.enrollment_repository.update_grade(enrollment_id, clean_grade)
        updated_enrollment = self.enrollment_repository.get_by_id(enrollment_id)
        if updated_enrollment is None:
            raise ValueError("Enrollment could not be loaded after grade update.")
        return updated_enrollment

    def list_students(self) -> list[Student]:
        return self.student_repository.get_all()

    def list_courses(self) -> list[Course]:
        return self.course_repository.get_all()

    def list_enrollments(self) -> list[Enrollment]:
        return self.enrollment_repository.get_all()
