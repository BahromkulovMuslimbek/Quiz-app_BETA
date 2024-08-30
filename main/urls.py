from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz-list', views.quizList, name='quizList'),
    path('quiz-detail/<int:id>/', views.quizDetail, name='quizDetail'),
    path('questionDelete/<int:id>/<int:pk>/', views.questionDelete, name='questionDelete'),
    path('optionDelete/<int:ques>/<int:option>/', views.deleteOption, name='optionDelete'),
    path('question-detail/<int:id>/', views.questionDetail, name='questionDetail'),
    path('create-quiz', views.createQuiz, name='createQuiz'),
    path('create-question/<int:id>/', views.questionCreate, name='questionCreate'),
]