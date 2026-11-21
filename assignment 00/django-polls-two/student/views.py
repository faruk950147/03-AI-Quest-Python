from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import F
from django.db import transaction
from django.views import View

from student.models import Question, Choice, Department, Student


class HomeView(View):
    def get(self, request):
        questions = Question.objects.prefetch_related("choices")
        students = Student.objects.select_related("department")

        return render(request, "home.html", {
            "questions": questions,
            "students": students,
        })


class VotingView(View):
    @transaction.atomic
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        choice_id = request.POST.get("choice")

        if not choice_id:
            return redirect("student:questions", pk=question.pk)

        choice = get_object_or_404(
            Choice,
            pk=choice_id,
            question=question,
        )

        choice.votes = F("votes") + 1
        choice.save()

        return redirect("student:questions", pk=question.pk)

class QuestionView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        choices = question.choices.all()

        return render(request, "question.html", {
            "question": question,
            "choices": choices,
        })


class DepartmentView(View):
    def get(self, request, pk):
        department = get_object_or_404(Department, pk=pk)

        return render(request, "department.html", {
            "department": department,
        })


class StudentView(View):
    def get(self, request, pk):
        student = get_object_or_404(
            Student.objects.select_related("department"),
            pk=pk,
        )

        return render(request, "student.html", {
            "student": student,
        })
