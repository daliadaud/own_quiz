from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    owner = models.ForeignKey(User, related_name='own_quizzes')
    description = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to="quiz_featured_images", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'quizzes'


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_questions')
    image = models.ImageField(upload_to='quiz_question_images', blank=True, null=True)
    question = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class QuestionChoiceAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='quiz_question_choice_answers')
    text_answer = models.TextField(blank=True)
    image_answer = models.ImageField(upload_to='quiz_question_answer_images', blank=True, null=True)
    value = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class QuizChoiceResult(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_results')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='quiz_result_images', blank=True, null=True)
    low_value = models.IntegerField()
    high_value = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class QuizInstance(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_instances')
    external_code = models.CharField(unique=True, max_length=50)
    user = models.ForeignKey(User, related_name='user_quiz_instances', blank=True, null=True) # to support anonymous user, user session instead
    is_completed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class QuizInstanceAnswer(models.Model):
    quiz_instance = models.ForeignKey(QuizQuestion, related_name='quiz_instance_answers')

    question = models.ForeignKey(QuizQuestion, related_name='quiz_instance_questions')
    answers = models.ForeignKey(QuestionChoiceAnswer, related_name='quiz_instance_answers')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
