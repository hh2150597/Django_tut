from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic

from .models import Quiz, Question, AnswerOption, UserAnswer, QuizResult

class QuizListView(generic.ListView):
    """
    View for listing all active quizzes.
    """
    model = Quiz
    template_name = "quiz/quiz_list.html"
    context_object_name = "quiz_list"

    def get_queryset(self):
        """
        Return only active quizzes.
        """
        return Quiz.objects.filter(pub_date__lte=timezone.now())

class QuizDetailView(generic.DetailView):
    """
    View for displaying a specific quiz and its questions.
    """
    model = Quiz
    template_name = "quiz/quiz_detail.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.filter(quiz=self.object).order_by("order")
        return context

def submit_quiz(request, quiz_id):
    """
    Process the submitted answers for a quiz and show the quiz results.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz).order_by("order")
    score = 0

    # Check user's answer for each question and update score
    for question in questions:
        selected_answer = request.POST.get(f"question_{question.id}")
        if selected_answer:
            selected_answer_obj = get_object_or_404(AnswerOption, pk=selected_answer)
            if selected_answer_obj.is_correct:
                score += 1

    # Create UserAnswer and QuizResult objects
    user = request.user
    for question in questions:
        selected_answer = request.POST.get(f"question_{question.id}")
        if selected_answer:
            UserAnswer.objects.create(user=user, question=question, selected_answer_id=selected_answer)
    QuizResult.objects.create(user=user, quiz=quiz, score=score)

    # Render quiz results page
    return render(request, "quiz/quiz_results.html", {"quiz": quiz, "score": score})
