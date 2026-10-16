
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F

from polls.models import Question, Choice


class HomePage(View):

    def get(self, request):
        questions = Question.objects.raw(
            """
            SELECT * FROM polls_question;
            """
        )

        context = {
            "questions": questions
        }

        return render(
            request,
            "polls/home.html",
            context
        )


class DetailPage(View):

    def get(self, request, pk):
        question = Question.objects.raw(
            """
            SELECT * FROM polls_question
            WHERE id = %s;
            """,
            [pk]
        )

        question = next(iter(question), None)

        if question is None:
            from django.http import Http404
            raise Http404("Question does not exist")

        context = {
            "question": question
        }

        return render(
            request,
            "polls/detail.html",
            context
        )


class VotingView(View):

    def post(self, request, pk):
        question = get_object_or_404(
            Question,
            pk=pk
        )

        try:
            selected_choice = question.choice_set.get(
                pk=request.POST["choice"]
            )

        except (KeyError, Choice.DoesNotExist):
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": (
                        "You didn't select a valid choice."
                    ),
                },
                status=400
            )

        selected_choice.votes = F("votes") + 1

        selected_choice.save(
            update_fields=["votes"]
        )

        return HttpResponseRedirect(
            reverse(
                "polls:results",
                args=[question.id]
            )
        )


class ResultsPage(View):

    def get(self, request, pk):
        question = Question.objects.raw(
            """
            SELECT * FROM polls_question
            WHERE id = %s;
            """,
            [pk]
        )

        question = next(iter(question), None)

        if question is None:
            from django.http import Http404
            raise Http404("Question does not exist")

        context = {
            "question": question
        }

        return render(
            request,
            "polls/results.html",
            context
        )