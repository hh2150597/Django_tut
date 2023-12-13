from django.urls import path

from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.QuizListView.as_view(), name="list"),
    path("<int:pk>/", views.QuizDetailView.as_view(), name="detail"),
    path("<int:quiz_id>/submit/", views.submit_quiz, name="submit"),
]
