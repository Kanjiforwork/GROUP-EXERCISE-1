from dataclasses import dataclass


@dataclass
class Student:
    id: int | None
    name: str
    email: str


@dataclass
class Course:
    id: int | None
    code: str
    title: str
    credits: int


@dataclass
class Enrollment:
    id: int | None
    student_id: int
    course_id: int
    grade: str | None
    enrolled_at: str
