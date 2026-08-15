from django.shortcuts import render, redirect
from .models import Quiz, Question, Choice, UserScore
from django.contrib.auth.decorators import login_required

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def start_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected:
                choice = Choice.objects.get(id=selected)
                if choice.is_correct:
                    score += 1
        UserScore.objects.create(user=request.user, quiz=quiz, score=score)
        return redirect('quiz_result', quiz_id=quiz.id)

    return render(request, 'quiz/start_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_result(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    score = UserScore.objects.filter(user=request.user, quiz=quiz).order_by('-date').first()
    return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'score': score})

def leaderboard(request):
    leaderboard = UserScore.objects.select_related('user', 'quiz').order_by('-score')[:10]
    return render(request, 'quiz/leaderboard.html', {'leaderboard': leaderboard})
