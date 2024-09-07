from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz-list/', views.quizList, name='quizList'),
    path('quiz/<int:id>/', views.quizDetail, name='quizDetail'),
    path('quiz/create/', views.quizCreate, name='quizCreate'),

    path('question/<int:id>/delete/<int:pk>/', views.questionDelete, name='questionDelete'),
    path('question/<int:id>/', views.questionDetail, name='questionDetail'),
    path('question/<int:id>/create/', views.questionCreate, name='questionCreate'),

    path('option/<int:ques>/delete/<int:option>/', views.optionDelete, name='optionDelete'),

    path('result/', views.results_list, name='results_list'),
    path('result/<int:id>/', views.results_detail, name='results_detail'),

    path('owner/result/<int:quiz_id>/', views.owner_results, name='owner_results'),
    path('owner/result/detail/<int:id>/', views.owner_results_detail, name='owner_results_detail'),

    path('quiz/<int:quiz_id>/export/excel/', views.export_quiz_answers_to_excel, name='export_quiz_answers_to_excel'),
    path('answer/<int:id>/export/excel/', views.export_answer_details_to_excel, name='export_answer_details_to_excel'),
    path('quiz/<int:quiz_id>/export/pdf/', views.export_quiz_to_pdf, name='export_quiz_to_pdf'),

]