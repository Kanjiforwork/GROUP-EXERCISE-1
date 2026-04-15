import pytest

from src.services.enrollment_service import EnrollmentService


@pytest.fixture
def service(tmp_path):
    database_path = tmp_path / "test_enrollment.db"
    return EnrollmentService(database_path=database_path)


def test_create_student_success(service):
    student = service.create_student("Alice Nguyen", "alice@example.com")

    assert student.id is not None
    assert student.name == "Alice Nguyen"
    assert student.email == "alice@example.com"


def test_create_course_success(service):
    course = service.create_course("CS101", "Introduction to Python", 3)

    assert course.id is not None
    assert course.code == "CS101"
    assert course.title == "Introduction to Python"
    assert course.credits == 3


def test_enroll_student_success(service):
    student = service.create_student("Alice Nguyen", "alice@example.com")
    course = service.create_course("CS101", "Introduction to Python", 3)

    enrollment = service.enroll_student(student.id, course.id)

    assert enrollment.id is not None
    assert enrollment.student_id == student.id
    assert enrollment.course_id == course.id
    assert enrollment.grade is None


def test_enroll_student_fails_when_student_does_not_exist(service):
    course = service.create_course("CS101", "Introduction to Python", 3)

    with pytest.raises(ValueError, match="Student with id 999 does not exist."):
        service.enroll_student(999, course.id)


def test_enroll_student_fails_when_course_does_not_exist(service):
    student = service.create_student("Alice Nguyen", "alice@example.com")

    with pytest.raises(ValueError, match="Course with id 999 does not exist."):
        service.enroll_student(student.id, 999)


def test_update_grade_success(service):
    student = service.create_student("Alice Nguyen", "alice@example.com")
    course = service.create_course("CS101", "Introduction to Python", 3)
    enrollment = service.enroll_student(student.id, course.id)

    updated_enrollment = service.update_grade(enrollment.id, "A")

    assert updated_enrollment.grade == "A"
