from django.conf.urls import include, url
from rest_framework import routers

from api.views import QuizViewSet, UserViewSet, quiz_start, quiz_instance

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, base_name="user")
router.register(r'quizzes', QuizViewSet, base_name="quiz")


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^quiz/(?P<quiz_id>[0-9]+)/start/$', quiz_start, name='quiz_start'),
    url(r'^quiz_instance/(?P<quiz_instance_id>[0-9]+)/$', quiz_instance, name='quiz_instance'),
    url(r'^quiz_instance/(?P<quiz_instance_id>[0-9]+)/submit/$', quiz_instance, name='quiz_instance_submit'),
]
