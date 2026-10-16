from django.urls import path

from polls.views import HomeView, QuestionDetailView, VoteView, ResultsView

app_name = "polls"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path(
        "<int:pk>/",
        QuestionDetailView.as_view(),
        name="detail"
    ),

    path(
        "<int:pk>/vote/",
        VoteView.as_view(),
        name="vote"
    ),

    path(
        "<int:pk>/results/",
        ResultsView.as_view(),
        name="results"
    ),
]