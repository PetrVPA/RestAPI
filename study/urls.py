from django.urls import path, include

from rest_framework.routers import SimpleRouter

from study.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)
#from study.apps import StudyConfig

#app_name = StudyConfig.name

app_name = "study"

router = SimpleRouter()
#router.register("", CourseViewSet, basename='course')
router.register(r'course', CourseViewSet, basename='course')


urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path(
        "lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path("", include(router.urls)),
]

#urlpatterns += router.urls
