from src.services.enrollment_service import EnrollmentService


MENU_TEXT = """
Student Course Enrollment
1. Create student
2. Create course
3. Enroll student in course
4. Update enrollment grade
5. List students
6. List courses
7. List enrollments
0. Exit
""".strip()


class EnrollmentCLI:
    def __init__(self, service: EnrollmentService | None = None) -> None:
        self.service = service or EnrollmentService()

    def run(self) -> None:
        while True:
            print()
            print(MENU_TEXT)
            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    self._create_student()
                elif choice == "2":
                    self._create_course()
                elif choice == "3":
                    self._enroll_student()
                elif choice == "4":
                    self._update_grade()
                elif choice == "5":
                    self._list_students()
                elif choice == "6":
                    self._list_courses()
                elif choice == "7":
                    self._list_enrollments()
                elif choice == "0":
                    print("Goodbye.")
                    break
                else:
                    print("Invalid choice. Please select a number from the menu.")
            except ValueError as exc:
                print(f"Error: {exc}")

    def _create_student(self) -> None:
        name = input("Student name: ")
        email = input("Student email: ")
        student = self.service.create_student(name, email)
        print(f"Created student #{student.id}: {student.name} ({student.email})")

    def _create_course(self) -> None:
        code = input("Course code: ")
        title = input("Course title: ")
        credits = int(input("Credits: ").strip())
        course = self.service.create_course(code, title, credits)
        print(f"Created course #{course.id}: {course.code} - {course.title}")

    def _enroll_student(self) -> None:
        student_id = int(input("Student id: ").strip())
        course_id = int(input("Course id: ").strip())
        enrollment = self.service.enroll_student(student_id, course_id)
        print(
            "Enrollment created: "
            f"#{enrollment.id} student={enrollment.student_id} course={enrollment.course_id}"
        )

    def _update_grade(self) -> None:
        enrollment_id = int(input("Enrollment id: ").strip())
        grade = input("Grade: ")
        enrollment = self.service.update_grade(enrollment_id, grade)
        print(f"Enrollment #{enrollment.id} grade updated to {enrollment.grade}")

    def _list_students(self) -> None:
        students = self.service.list_students()
        if not students:
            print("No students found.")
            return

        for student in students:
            print(f"#{student.id}: {student.name} - {student.email}")

    def _list_courses(self) -> None:
        courses = self.service.list_courses()
        if not courses:
            print("No courses found.")
            return

        for course in courses:
            print(
                f"#{course.id}: {course.code} - {course.title} ({course.credits} credits)"
            )

    def _list_enrollments(self) -> None:
        enrollments = self.service.list_enrollments()
        if not enrollments:
            print("No enrollments found.")
            return

        for enrollment in enrollments:
            print(
                f"#{enrollment.id}: student={enrollment.student_id}, "
                f"course={enrollment.course_id}, grade={enrollment.grade}, "
                f"enrolled_at={enrollment.enrolled_at}"
            )
