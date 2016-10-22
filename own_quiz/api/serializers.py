from quiz.models import Quiz, QuizQuestion, QuestionChoiceAnswer, QuizChoiceResult, QuizInstance, QuizInstanceAnswer
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class QuestionChoiceAnswerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = QuestionChoiceAnswer
        fields = ('id', 'text_answer', 'image_answer', 'value')


class QuizQuestionSerializer(serializers.HyperlinkedModelSerializer):
    quiz_question_choice_answers = QuestionChoiceAnswerSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = ('id', 'image', 'question', 'quiz_question_choice_answers')


class QuizChoiceResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = QuizChoiceResult
        fields = ('id', 'description', 'image', 'low_value', 'high_value')


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()
    quiz_questions = QuizQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'slug', 'owner', 'description', 'featured_image', 'quiz_questions')


class QuizInstanceAnswerSerializer(serializers.HyperlinkedModelSerializer):
    question = QuizQuestionSerializer()
    answer = QuestionChoiceAnswerSerializer()

    class Meta:
        model = QuizInstanceAnswer
        fields = ('question', 'answer')


class QuizInstanceSerializer(serializers.HyperlinkedModelSerializer):
    quiz_instance_answers = QuizInstanceAnswerSerializer(many=True)
    quiz_result = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = QuizInstance
        fields = ('id', 'external_code', 'user', 'is_completed', 'quiz_instance_answers', 'quiz_result', 'total_value')

    def get_total_value(self, obj):
        return obj.get_result_value()

    def get_quiz_result(self, obj):
        result_value = obj.get_result_value()
        quiz = obj.quiz

        result = quiz.get_quiz_result(value=result_value)

        if result:
            serializer = QuizChoiceResultSerializer(result)
            return serializer.data
        return ""


class QuizInstanceSubmitAnswerSerializer(serializers.Serializer):
    quiz_instance_answers = serializers.JSONField(required=True)

    def validate_quiz_instance_answers(self, quiz_instance_answers):
        # validate if quiz answer is owned by quiz question
        quiz_instance = self.context['quiz_instance']
        cleaned_quiz_instance_answers, error = quiz_instance.validate_quiz_instance(data=quiz_instance_answers)
        if error:
            raise serializers.ValidationError(error)
        return cleaned_quiz_instance_answers