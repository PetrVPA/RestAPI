import stripe
from django.http import JsonResponse
from rest_framework import viewsets, generics
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from study.models import Subscription

from study.models import Course, Lesson
from study.paginators import CustomPagination
from study.serializer import (
    CourseSerializer,
    LessonSerializer,
    CourseCountLessonSerializer,
)

from users.permissions import IsModerator, IsOwner, IsNotModerator

from users.services import create_stripe_checkout_session

stripe.api_key = settings.STRIPE_SECRET_KEY


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
    pagination_class = CustomPagination

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
            # Создавать могут только авторизованные, но не модераторы
            permission_classes = [IsNotModerator]
        elif self.action in ['update', 'partial_update', 'retrieve', 'list']:
            permission_classes = [IsModerator | IsOwner]
        elif self.action in ['destroy']:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        # 1. Берем базовый список всех уроков
        queryset = Lesson.objects.all()

        # 2. ДОБАВЛЯЕМ ФИЛЬТРАЦИЮ ПО КУРСУ (то, что вы хотите проверить)
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # 3. ПРИМЕНЯЕМ ПРАВА ДОСТУПА (ваша существующая логика)
        if user.groups.filter(name='moderators').exists():
            # Модератор видит отфильтрованные уроки (все или по конкретному курсу)
            return queryset

        # Обычный пользователь видит только свои отфильтрованные уроки
        return queryset.filter(owner=user)


    def perform_create(self, serializer):
        # При создании урока автоматически назначаем владельцем текущего пользователя
        serializer.save(owner=self.request.user)


    def get_permissions(self):
        # Безопасно получаем текущее действие (если его нет, будет None)
        action = getattr(self, 'action', None)

        if action == 'create':
            # Создавать могут только авторизованные, но не модераторы
            permission_classes = [IsNotModerator]
        elif action in ['update', 'partial_update', 'retrieve', 'list']:
            permission_classes = [IsModerator | IsOwner]
        elif action == 'destroy':
            permission_classes = [IsOwner]
        else:
            # Если action не определился (что маловероятно), берем базовые настройки
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]


class SubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        # Берем ID курса из ТЕЛА запроса
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'Необходимо передать course_id в теле запроса'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ищем курс в базе. Если нет — вернется 404 (но уже от Django, а не роутера)
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})
