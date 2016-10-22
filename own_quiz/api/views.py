from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from quiz.models import Quiz, QuizInstance, QuizQuestion, QuestionChoiceAnswer, QuizInstanceAnswer
from .serializers import QuizSerializer, UserSerializer, QuizInstanceSerializer, QuizInstanceSubmitAnswerSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(is_active=True)


@api_view(['POST'])
@permission_classes((AllowAny,))
def quiz_start(request, quiz_id, **kwargs):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    quiz_taker = None
    user = request.user
    if user.is_authenticated:
        quiz_taker = user

    quiz_instance = QuizInstance.create_quiz_instance(quiz=quiz, user=quiz_taker)
    serializer = QuizInstanceSerializer(quiz_instance, context={'request': request})

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def quiz_instance(request, quiz_instance_id, **kwargs):
    quiz_instance = get_object_or_404(QuizInstance, pk=quiz_instance_id)
    context = {}
    context['request'] = request
    quiz_instance_serializer = QuizInstanceSerializer(quiz_instance, context=context)
    if request.method == 'GET':
        return Response(quiz_instance_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        context['quiz_instance'] = quiz_instance
        serializer = QuizInstanceSubmitAnswerSerializer(data=request.data, context=context)
        if serializer.is_valid():
            quiz_instance_answers = serializer.validated_data.get('quiz_instance_answers')
            for key, value in quiz_instance_answers.items():
                question = QuizQuestion.objects.get(pk=key)
                answer = QuestionChoiceAnswer.objects.get(pk=value)
                quiz_instance_answer = QuizInstanceAnswer.objects.get(quiz_instance=quiz_instance, question=question)
                quiz_instance_answer.submit_answer(answer=answer)
            quiz_instance.set_completed()

            return Response(quiz_instance_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)