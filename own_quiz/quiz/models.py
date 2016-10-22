from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    owner = models.ForeignKey(User, related_name='own_quizzes')
    description = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to="quiz_featured_images", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'quizzes'

    def __str__(self):
        return self.title

    def get_question_ids(self):
        return QuizQuestion.objects.filter(quiz=self).values_list('pk', flat=True)

    def get_quiz_result(self, value):
        quiz_choice_results = QuizChoiceResult.objects.filter(quiz=self)
        for choice_result in quiz_choice_results:
            if choice_result.is_value_in_range(value=value):
                return choice_result
        return None


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_questions')
    image = models.ImageField(upload_to='quiz_question_images', blank=True, null=True)
    question = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_choice_answer_ids(self):
        return QuestionChoiceAnswer.objects.filter(question=self).values_list('pk', flat=True)

    def __str__(self):
        return self.question


class QuestionChoiceAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='quiz_question_choice_answers')
    text_answer = models.TextField(blank=True)
    image_answer = models.ImageField(upload_to='quiz_question_answer_images', blank=True, null=True)
    value = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text_answer


class QuizChoiceResult(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_results')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='quiz_result_images', blank=True, null=True)
    low_value = models.IntegerField()
    high_value = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_value_in_range(self, value):
        if self.low_value <= value <= self.high_value:
            return True
        return False

    # quiz choice answer low and high value must not overlap


class QuizInstance(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz_instances')
    external_code = models.CharField(unique=True, max_length=50) # code used to share externally
    user = models.ForeignKey(User, related_name='user_quiz_instances', blank=True, null=True) # to support anonymous user, user session instead
    is_completed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_result_value(self):
        value = 0
        quiz_instance_answers = QuizInstanceAnswer.objects.filter(quiz_instance=self)
        for quiz_instance_answer in quiz_instance_answers:
            if quiz_instance_answer.answer:
                answer = quiz_instance_answer.answer
                value = value + answer.value
        return value

    @staticmethod
    def create_quiz_instance(quiz, user=None):
        while True:
            external_code = get_random_string()
            try:
                QuizInstance.objects.get(external_code=external_code)
            except QuizInstance.DoesNotExist:
                break

        instance = QuizInstance.objects.create(quiz=quiz, user=user, external_code=external_code)
        quiz_questions = QuizQuestion.objects.filter(quiz=quiz)

        for question in quiz_questions:
            QuizInstanceAnswer.create_quiz_instance_answer(quiz_instance=instance, question=question)

        return instance

    def incomplete_entries(self):
        return QuizInstanceAnswer.objects.filter(quiz_instance=self, answer=None)

    def set_completed(self):
        if not self.incomplete_entries():
            self.is_completed = True
            self.save()

    def validate_quiz_instance(self, data):
        error_message = {}
        l = []
        question_ids = self.quiz.get_question_ids()
        for question_id in question_ids:
            # check if all question is submitted
            key_list = list(map(int, data.keys()))
            if question_id not in key_list:
                l.append('This question is required')
                error_message[question_id] = l
            if error_message:
                return data, error_message

        for key, value in data.items():
            # check if all there's any invalid question submitted
            if int(key) not in question_ids:
                l.append('Invalid Question Id')
                error_message[key] = l
        if error_message:
                return data, error_message

        # if no invalid question id and all questions id are supplied
        for key, value in data.items():
            question = QuizQuestion.objects.get(pk=key)
            if value not in question.get_choice_answer_ids():
                l.append('Invalid Answer Id')
                error_message[key] = l
        if error_message:
            return data, error_message

        return data, None  # No error


class QuizInstanceAnswer(models.Model):  # rename to QuizInstanceEntries
    quiz_instance = models.ForeignKey(QuizInstance, related_name='quiz_instance_answers')

    question = models.ForeignKey(QuizQuestion, related_name='quiz_instance_questions')
    answer = models.ForeignKey(QuestionChoiceAnswer, related_name='quiz_instance_answers', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('question', 'quiz_instance')

    @staticmethod
    def create_quiz_instance_answer(quiz_instance, question, answer=None):
        return QuizInstanceAnswer.objects.create(quiz_instance=quiz_instance, question=question, answer=answer)

    def submit_answer(self, answer):
        if not self.quiz_instance.is_completed:
            question_choice_answers = QuestionChoiceAnswer.objects.filter(question=self.question)
            if answer in question_choice_answers:
                self.answer = answer
                self.save()
