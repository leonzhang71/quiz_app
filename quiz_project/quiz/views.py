from django.shortcuts import render

from .models import Question, Choice


def quiz(request):
    """
    Display all questions with choices and compute the score when submitted.
    """
    if request.method == "POST":
        questions = Question.objects.prefetch_related("choices").all()
        score = 0
        total = 0
        for question in questions:
            total += question.points
            selected_choice_id = request.POST.get(str(question.id))
            if selected_choice_id:
                try:
                    choice = Choice.objects.get(id=selected_choice_id, question=question)
                    if choice.is_correct:
                        score += question.points
                except Choice.DoesNotExist:
                    pass

        return render(request, "quiz/result.html", {"score": score, "total": total})

    questions = Question.objects.prefetch_related("choices").all()
    return render(request, "quiz/quiz.html", {"questions": questions})
