from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz-list/', views.quizList, name='quizList'),
    path('quiz-detail/<int:id>/', views.quizDetail, name='quizDetail'),
    path('quiz-create/', views.quizCreate, name='createQuiz'),

    path('question-delete/<int:id>/<int:pk>/', views.questionDelete, name='questionDelete'),
    path('question-detail/<int:id>/', views.questionDetail, name='questionDetail'),
    path('question-create/<int:id>/', views.questionCreate, name='questionCreate'),

    path('option-delete/<int:ques>/<int:option>/', views.optionDelete, name='optionDelete'),
]