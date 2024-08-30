from django.shortcuts import render, redirect
from main import models


def getQuiz(request, id):
    quiz = models.Quiz.objects.get(id=id)
    return render(request, 'answer/get-quiz.html', {'quiz':quiz})

def makeAnswer(request, id):
    quiz = models.Quiz.objects.get(id=id)
    answer = models.Answer.objects.create(quiz=quiz, author=request.user)
    for key, value in request.POST.items():
        if key.isdigit():
            models.AnswerDetail.objects.create(
                answer=answer, 
                question=models.Question.objects.get(id=int(key)), 
                user_choice=models.Option.objects.get(id=int(value)))
    return redirect('getQuiz', quiz.id)