from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz, Question,Result
from django.contrib.auth.forms import UserCreationForm

def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizzes': quizzes})



@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if Result.objects.filter(user=request.user, quiz=quiz).exists():
        messages.warning(request, "You have already attempted this quiz.")
        return redirect("leaderboard", quiz.id)
    
    questions = Question.objects.filter(quiz=quiz)


    if request.method == "POST":

        # ✅ SAFETY CHECK
        answered = False
        score = 0
        
        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected:
                answered = True
                if selected == q.correct_option:
                    score += 1

        # ❌ Prevent empty auto-submit
        if not answered:
            return render(request, "quiz/take_quiz.html", {
                "quiz": quiz,
                "questions": questions,
            })

        Result.objects.create(
            user=request.user,
            quiz=quiz,
            score=score
        )

        return redirect("result", quiz.id)

    return render(request, "quiz/take_quiz.html", {
        "quiz": quiz,
        "questions": questions,
    })


@login_required
def result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    result = Result.objects.filter(user=request.user, quiz=quiz).last()

    return render(request, 'quiz/result.html', {
        'quiz': quiz,
        'result': result
    })


def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    results = Result.objects.filter(
        quiz=quiz
    ).select_related("user").order_by(
        "-score", "created_at"
    )

    return render(request, "quiz/leaderboard.html", {
        "quiz": quiz,
        "results": results
    })

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please login.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
