from pathlib import Path

from src.data.database import DATABASE_PATH, get_connection
from src.domain.entities import Course


class CourseRepository:
    def __init__(self, database_path: str | Path = DATABASE_PATH) -> None:
        self.database_path = database_path

    def create(self, code: str, title: str, credits: int) -> Course:
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                "INSERT INTO courses (code, title, credits) VALUES (?, ?, ?)",
                (code, title, credits),
            )
            course_id = cursor.lastrowid

        return Course(id=course_id, code=code, title=title, credits=credits)

    def get_by_id(self, course_id: int) -> Course | None:
        with get_connection(self.database_path) as connection:
            row = connection.execute(
                "SELECT id, code, title, credits FROM courses WHERE id = ?",
                (course_id,),
            ).fetchone()

        if row is None:
            return None

        return Course(
            id=row["id"],
            code=row["code"],
            title=row["title"],
            credits=row["credits"],
        )

    def get_all(self) -> list[Course]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                "SELECT id, code, title, credits FROM courses ORDER BY id"
            ).fetchall()

        return [
            Course(
                id=row["id"],
                code=row["code"],
                title=row["title"],
                credits=row["credits"],
            )
            for row in rows
        ]

    def delete(self, course_id: int) -> bool:
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                "DELETE FROM courses WHERE id = ?",
                (course_id,),
            )

        return cursor.rowcount > 0
