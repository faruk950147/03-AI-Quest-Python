from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render  # <-- Added redirect
from django.urls import reverse
from django.views import View

from polls.models import Choice, Question


class HomePage(View):
    def get(self, request):
        questions = Question.objects.raw(
            """
            SELECT * FROM polls_question;
            """
        )

        context = {"questions": questions}

        return render(request, "polls/home.html", context)


class DetailPage(View):
    def get(self, request, pk):
        question = Question.objects.raw(
            """
            SELECT * FROM polls_question
            WHERE id = %s;
            """,
            [pk],
        )

        question = next(iter(question), None)

        if question is None:
            raise Http404("Question does not exist")

        context = {"question": question}

        return render(request, "polls/detail.html", context)


class VotingView(View):

    def post(self, request, pk):
        question = Question.objects.raw(
            """
            SELECT * FROM polls_question
            WHERE id = %s;
            """,
            [pk],
        )

        # Unwrap the RawQuerySet to get the actual Question instance
        question = next(iter(question), None)

        if question is None:
            raise Http404("Question does not exist")

        choice_id = request.POST.get("choice")

        if not choice_id:
            return redirect("polls:detail", pk=question.id)

        selected_choice = question.choice_set.filter(pk=choice_id).first()

        if selected_choice is None:
            return redirect("polls:detail", pk=question.id)

        selected_choice.votes = F("votes") + 1
        selected_choice.save(update_fields=["votes"])

        return HttpResponseRedirect(
            reverse("polls:results", args=[question.id])
        )


class ResultsPage(View):

    def get(self, request, pk):
        question = Question.objects.raw(
            """
            SELECT * FROM polls_question
            WHERE id = %s;
            """,
            [pk],
        )

        question = next(iter(question), None)

        if question is None:
            raise Http404("Question does not exist")

        context = {"question": question}

        return render(request, "polls/results.html", context)
