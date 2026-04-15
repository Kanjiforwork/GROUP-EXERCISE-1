from pathlib import Path

from src.data.database import DATABASE_PATH, get_connection
from src.domain.entities import Student


class StudentRepository:
    def __init__(self, database_path: str | Path = DATABASE_PATH) -> None:
        self.database_path = database_path

    def create(self, name: str, email: str) -> Student:
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                "INSERT INTO students (name, email) VALUES (?, ?)",
                (name, email),
            )
            student_id = cursor.lastrowid

        return Student(id=student_id, name=name, email=email)

    def get_by_id(self, student_id: int) -> Student | None:
        with get_connection(self.database_path) as connection:
            row = connection.execute(
                "SELECT id, name, email FROM students WHERE id = ?",
                (student_id,),
            ).fetchone()

        if row is None:
            return None

        return Student(id=row["id"], name=row["name"], email=row["email"])

    def get_all(self) -> list[Student]:
        with get_connection(self.database_path) as connection:
            rows = connection.execute(
                "SELECT id, name, email FROM students ORDER BY id"
            ).fetchall()

        return [
            Student(id=row["id"], name=row["name"], email=row["email"])
            for row in rows
        ]

    def delete(self, student_id: int) -> bool:
        with get_connection(self.database_path) as connection:
            cursor = connection.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,),
            )

        return cursor.rowcount > 0
