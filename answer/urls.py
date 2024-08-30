from django.urls import path
from . import views

urlpatterns = [
    path('get-quiz/<int:id>', views.getQuiz, name='getQuiz'),
    path('make-answer/<int:id>', views.makeAnswer, name='makeAnswer'),
]