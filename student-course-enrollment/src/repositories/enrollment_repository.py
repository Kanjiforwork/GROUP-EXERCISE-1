from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from src.data.database import DATABASE_PATH, get_connection
from src.domain.entities import Enrollment


class EnrollmentRepository:
    def __init__(self, database_path: str | Path = DATABASE_PATH) -> None:
        self.database_path = database_path

    def enroll(self, student_id: int, course_id: int) -> Enrollment:
        enrolled_at = datetime.now(timezone.utc).isoformat()

        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO enrollments (student_id, course_id, enrolled_at)
                VALUES (?, ?, ?)
                """,
                (student_id, course_id, enrolled_at),
            )
            enrollment_id = cursor.lastrowid

        return Enrollment(
            id=enrollment_id,
            student_id=student_id,
            course_id=course_id,
            grade=None,
            enrolled_at=enrolled_at,
        )

    def get_all(self) -> list[Enrollment]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, student_id, course_id, grade, enrolled_at
                FROM enrollments
                ORDER BY id
                """
            ).fetchall()

        return [self._row_to_enrollment(row) for row in rows]

    def get_by_id(self, enrollment_id: int) -> Enrollment | None:
        with get_connection(self.database_path) as connection:
            row = connection.execute(
                """
                SELECT id, student_id, course_id, grade, enrolled_at
                FROM enrollments
                WHERE id = ?
                """,
                (enrollment_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_enrollment(row)

    def get_by_student(self, student_id: int) -> list[Enrollment]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                """
                SELECT id, student_id, course_id, grade, enrolled_at
                FROM enrollments
                WHERE student_id = ?
                ORDER BY id
                """,
                (student_id,),
            ).fetchall()

        return [self._row_to_enrollment(row) for row in rows]

    def update_grade(self, enrollment_id: int, grade: str) -> bool:
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                "UPDATE enrollments SET grade = ? WHERE id = ?",
                (grade, enrollment_id),
            )

        return cursor.rowcount > 0

    def delete(self, enrollment_id: int) -> bool:
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                "DELETE FROM enrollments WHERE id = ?",
                (enrollment_id,),
            )

        return cursor.rowcount > 0

    def _row_to_enrollment(self, row: sqlite3.Row) -> Enrollment:
        return Enrollment(
            id=row["id"],
            student_id=row["student_id"],
            course_id=row["course_id"],
            grade=row["grade"],
            enrolled_at=row["enrolled_at"],
        )
