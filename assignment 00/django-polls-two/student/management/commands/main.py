
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from student.models import Question, Choice, Department, Student


class Command(BaseCommand):
    help = "Populate the database with sample data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # 1. Create sample questions and choices
        questions_data = {
            "What is your favorite color?": [
                "Red",
                "Blue",
                "Green",
            ],
            "What is your favorite animal?": [
                "Dog",
                "Cat",
                "Bird",
            ],
            "What is your favorite programming language?": [
                "Python",
                "JavaScript",
                "Java",
            ],
        }

        for question_text, choices in questions_data.items():
            question, created = Question.objects.get_or_create(
                question_text=question_text,
                defaults={
                    "pub_date": timezone.now(),
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created question: {question.question_text}"
                    )
                )

            for choice_text in choices:
                choice, choice_created = Choice.objects.get_or_create(
                    question=question,
                    choice_text=choice_text,
                )

                if choice_created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created choice: {choice.choice_text}"
                        )
                    )

        # 2. Create sample departments
        departments_data = [
            {
                "name": "Computer Science",
                "seat": 60,
            },
            {
                "name": "Mathematics",
                "seat": 40,
            },
        ]

        departments = {}

        for department_data in departments_data:
            department, created = Department.objects.get_or_create(
                name=department_data["name"],
                defaults={
                    "seat": department_data["seat"],
                },
            )

            departments[department.name] = department

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created department: {department.name}"
                    )
                )

        # 3. Create sample students
        students_data = [
            {
                "name": "Alice",
                "age": 22,
                "department": "Computer Science",
            },
            {
                "name": "Bob",
                "age": 24,
                "department": "Mathematics",
            },
        ]

        for student_data in students_data:
            department = departments[student_data["department"]]

            student, created = Student.objects.get_or_create(
                name=student_data["name"],
                department=department,
                defaults={
                    "age": student_data["age"],
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created student: {student.name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with sample data!"
            )
        )
