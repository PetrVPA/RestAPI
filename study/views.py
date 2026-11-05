from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from study.models import Course, Lesson
from study.serializer import (
    CourseSerializer,
    LessonSerializer,
    CourseCountLessonSerializer,
)
from users.permissions import IsModerator, IsOwner


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        # Если пользователь модератор — показываем все курсы
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        # Обычный пользователь видит только свои курсы
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        # При создании курса автоматически назначаем владельцем текущего пользователя
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Создавать могут только авторизованные (или админы)
            permission_classes = [IsAuthenticated]  # Или IsAdminUser
        elif self.action in ['update', 'partial_update', 'retrieve']:
            # Редактировать/просматривать может модератор ИЛИ владелец
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        else:
            # Список (list) доступен всем авторизованным (фильтрация идет в get_queryset)
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
