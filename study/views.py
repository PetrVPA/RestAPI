from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated


from study.models import Course, Lesson
from study.serializer import (
    CourseSerializer,
    LessonSerializer,
    CourseCountLessonSerializer,
)
from users.permissions import IsModerator, IsOwner


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDestroyAPIView(generics.DestroyAPIView):
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
        if self.action in ['create']:
            # Создавать могут только авторизованные пользователи)
            permission_classes = [IsAuthenticated or not IsModerator]  # админы не могут создавать IsAdminUser
        elif self.action in ['update', 'partial_update', 'retrieve', 'list']:
            # Редактировать/просматривать может модератор ИЛИ владелец
            permission_classes = [IsModerator | IsOwner]
        elif self.action in ['destroy']:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        # Если пользователь модератор — показываем все уроки
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        # Обычный пользователь видит только свои уроки
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        # При создании урока автоматически назначаем владельцем текущего пользователя
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            # Создавать могут только авторизованные пользователи)
            permission_classes = [IsAuthenticated or not IsModerator]  # админы не могут создавать IsAdminUser
        elif self.action in ['update', 'partial_update', 'retrieve', 'list']:
            # Редактировать/просматривать может модератор ИЛИ владелец
            permission_classes = [IsModerator | IsOwner]
        elif self.action in ['destroy']:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]
