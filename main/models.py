from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def questions_count(self):
        return self.question_set.count()


class Question(models.Model):
    name = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def correct_option(self):
        return self.option_set.get(correct=True)


class Option(models.Model):
    name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_late = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.author.username} -> {self.quiz.name}"

    @property
    def correct_answers_count(self):
        return self.answerdetail_set.filter(user_choice__correct=True).count()

    @property
    def incorrect_answers_count(self):
        return self.answerdetail_set.filter(user_choice__correct=False).count()

    @property
    def correct_answers_percentage(self):
        total_questions = self.quiz.questions_count
        return (self.correct_answers_count / total_questions) * 100


class AnswerDetail(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_choice = models.ForeignKey(Option, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        assert not AnswerDetail.objects.filter(answer=self.answer, question=self.question).exists(), "Bu savolga javob berilgan"
        super().save(*args, **kwargs)

    @property
    def is_correct(self):
        return self.user_choice.correct