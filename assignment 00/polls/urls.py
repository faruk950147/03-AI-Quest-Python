from django.urls import path

from polls.views import (
    HomePage,
    DetailPage,
    VoteView,
    ResultsPage,
)

app_name = "polls"

urlpatterns = [
    path("", HomePage.as_view(), name="home"),

    path(
        "<int:pk>/",
        DetailPage.as_view(),
        name="detail"
    ),

    path(
        "<int:pk>/vote/",
        VoteView.as_view(),
        name="vote"
    ),

    path(
        "<int:pk>/results/",
        ResultsPage.as_view(),
        name="results"
    ),
]