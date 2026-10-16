from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from polls.models import Choice, Question


class HomeView(View):

    def get(self, request):
        questions = Question.objects.order_by("-pub_date")
        return render(request, "polls/home.html", {"questions": questions})


class QuestionDetailView(View):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(request, "polls/detail.html", {"question": question})


class VoteView(View):

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        choice_id = request.POST.get("choice")

        if not choice_id:
            return redirect("polls:detail", pk=question.id)

        choice = get_object_or_404(Choice, pk=choice_id, question=question)

        # Race-condition safe vote increment using F() expressions
        Choice.objects.filter(pk=choice.pk).update(votes=F("votes") + 1)

        return redirect("polls:results", pk=question.pk)


class ResultsView(View):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(request, "polls/results.html", {"question": question})
