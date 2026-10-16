import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_future_question_is_not_recent(self):
        future_time = timezone.now() + datetime.timedelta(days=30)

        question = Question(
            question_text="Future question",
            pub_date=future_time,
        )

        self.assertIs(
            question.was_published_recently(),
            False,
        )

    def test_old_question_is_not_recent(self):
        old_time = timezone.now() - datetime.timedelta(
            days=1,
            seconds=1,
        )

        question = Question(
            question_text="Old question",
            pub_date=old_time,
        )

        self.assertIs(
            question.was_published_recently(),
            False,
        )

    def test_recent_question_is_recent(self):
        recent_time = timezone.now() - datetime.timedelta(
            hours=1,
        )

        question = Question(
            question_text="Recent question",
            pub_date=recent_time,
        )

        self.assertIs(
            question.was_published_recently(),
            True,
        )


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(
            reverse("polls:home")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "No polls are available.",
        )

    def test_invalid_question_returns_404(self):
        response = self.client.get(
            reverse("polls:detail", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_vote_requires_valid_choice(self):
        question = Question.objects.create(
            question_text="Favourite language?",
            pub_date=timezone.now(),
        )

        response = self.client.post(
            reverse("polls:vote", args=[question.pk]),
            {},
        )

        self.assertEqual(response.status_code, 400)
