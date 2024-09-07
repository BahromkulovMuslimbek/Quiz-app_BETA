from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from random import choice, sample
from xhtml2pdf import pisa
from . import models
import openpyxl


def index(request):
    return render(request, 'index.html')


def quizList(request):
    images = [
        'https://st2.depositphotos.com/2769299/7314/i/450/depositphotos_73146775-stock-photo-a-stack-of-books-on.jpg',
        'https://img.freepik.com/free-photo/creative-composition-world-book-day_23-2148883765.jpg',
        'https://profit.pakistantoday.com.pk/wp-content/uploads/2018/04/Stack-of-books-great-education.jpg',
        'https://live-production.wcms.abc-cdn.net.au/73419a11ea13b52c6bd9c0a69c10964e?impolicy=wcms_crop_resize&cropH=1080&cropW=1918&xPos=1&yPos=0&width=862&height=485',
        'https://live-production.wcms.abc-cdn.net.au/398836216839841241467590824c5cf1?impolicy=wcms_crop_resize&cropH=2813&cropW=5000&xPos=0&yPos=0&width=862&height=485',
        'https://images.theconversation.com/files/45159/original/rptgtpxd-1396254731.jpg?ixlib=rb-4.1.0&q=45&auto=format&w=1356&h=668&fit=crop'
    ]

    quizes = models.Quiz.objects.filter(author=request.user)
    quizes_list = []

    for quiz in quizes:
        quiz.img = choice(images)
        quizes_list.append(quiz)

    return render(request, 'quiz/quiz-list.html', {'quizes': quizes_list})


def quizDetail(request, id):
    quiz = get_object_or_404(models.Quiz, id=id)
    return render(request, 'quiz/quiz-detail.html', {'quiz': quiz})


def questionDelete(request, id, pk):
    question = get_object_or_404(models.Question, id=id)
    if request.method == 'POST':
        question.delete()
        return redirect('quizDetail', id=pk)


def quizCreate(request):
    if request.method == 'POST':
        quiz = models.Quiz.objects.create(
            name=request.POST['name'],
            amount=request.POST['amount'],
            author=request.user
        )
        return redirect('quizDetail', quiz.id)
    return render(request, 'quiz/quiz-create.html')


def questionCreate(request, id):
    quiz = get_object_or_404(models.Quiz, id=id)
    if request.method == 'POST':
        question_text = request.POST['name']
        true = request.POST['true']
        false_list = request.POST.getlist('false-list')

        question = models.Question.objects.create(
            name=question_text,
            quiz=quiz,
        )

        models.Option.objects.create(
            question=question,
            name=true,
            correct=True,
        )

        for false in false_list:
            models.Option.objects.create(
                name=false,
                question=question,
            )
        return redirect('quizDetail', id=quiz.id)

    return render(request, 'question/question-create.html', {'quiz': quiz})


def questionDetail(request, id):
    question = get_object_or_404(models.Question, id=id)
    return render(request, 'question/question-detail.html', {'question': question})


def optionDelete(request, ques, option):
    question = get_object_or_404(models.Question, id=ques)
    option = get_object_or_404(models.Option, question=question, id=option)
    option.delete()
    return redirect('questionDetail', id=ques)


def results_list(request):
    answers = models.Answer.objects.filter(author=request.user)
    return render(request, 'result/result_list.html', {'answers': answers})


def results_detail(request, id):
    answer = get_object_or_404(models.Answer, id=id)
    details = models.AnswerDetail.objects.filter(answer=answer)
    return render(request, 'result/result_detail.html', {'answer': answer, 'details': details})


def owner_results(request, quiz_id):
    quiz = get_object_or_404(models.Quiz, id=quiz_id)
    answers = models.Answer.objects.filter(quiz=quiz)
    return render(request, 'owner/owner_result.html', {'quiz': quiz, 'answers': answers})


def owner_results_detail(request, id):
    answer = get_object_or_404(models.Answer, id=id)
    details = models.AnswerDetail.objects.filter(answer=answer)
    return render(request, 'owner/owner_result_detail.html', {'answer': answer, 'details': details})


def export_quiz_answers_to_excel(request, quiz_id):
    quiz = get_object_or_404(models.Quiz, id=quiz_id)
    answers = models.Answer.objects.filter(quiz=quiz)
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = f"Javoblar {quiz.name} uchun"
    worksheet.append(["#", "Foydalanuvchi ismi", "To'g'ri javoblar soni", "Xato javoblar soni", "To'g'ri javoblar foizi (%)"])

    for idx, answer in enumerate(answers, 1):
        worksheet.append([
            idx,
            answer.author.username,
            answer.correct_answers_count,
            answer.incorrect_answers_count,
            answer.correct_answers_percentage
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={quiz.name}_javoblar.xlsx'
    workbook.save(response)
    return response


def export_answer_details_to_excel(request, id):
    answer = get_object_or_404(models.Answer, id=id)
    details = models.AnswerDetail.objects.filter(answer=answer)
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = f"Javoblar {answer.quiz.name} uchun"
    worksheet.append(["#", "Savol nomi", "Foydalanuvchi tanlovi", "Holat (To'g'ri/Xato)"])

    for idx, detail in enumerate(details, 1):
        worksheet.append([
            idx,
            detail.question.name,
            detail.user_choice.name,
            "To'g'ri" if detail.is_correct else "Xato"
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={answer.quiz.name}_javob_tafsilotlari.xlsx'
    workbook.save(response)
    return response


def export_quiz_to_pdf(request, quiz_id):
    quiz = get_object_or_404(models.Quiz, id=quiz_id)
    answers = models.Answer.objects.filter(quiz=quiz)

    html = render_to_string('quiz/quiz_pdf_template.html', {'quiz': quiz, 'answers': answers})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={quiz.name}.pdf'

    pisa.CreatePDF(html, dest=response)
    return response