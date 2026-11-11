from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from users.serializers import PaymentSerializer  # Убедитесь, что он существует
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Student
from .serializers import StudentRegisterSerializer, StudentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from study.models import Course
from django.shortcuts import get_object_or_404
from rest_framework import status
import datetime
from users.services import create_stripe_checkout_session, get_stripe_payment_status


class CreatePaymentView(APIView):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        # ПРОВЕРКА: есть ли уже оплаченный платеж за этот курс?
        # Ищем платеж, где is_paid=True и study_course=course
        already_paid = Payment.objects.filter(
            user=request.user,
            study_course=course,
            is_paid=True
        ).exists()

        if already_paid:
            return Response(
                {"error": "Вы уже приобрели этот курс"},
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # 1. Подключаем бэкенды фильтрации и сортировки
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    # 2. Настраиваем фильтрацию (по каким полям можно фильтровать)
    filterset_fields = {
        'category_payment': ['exact'],  # Фильтр по ID курса

        'payment_option': ['exact'],  # Фильтр по способу оплаты
        # Если у вас есть поле category_payment, его тоже можно добавить
        # 'category_payment': ['exact'],
    }

    # 3. Настраиваем сортировку (по какому полю можно сортировать)
    ordering_fields = ('date_payment',)
    ordering = ('-date_payment',)  # Сортировка по умолчанию (новые сверху, знак минуса)
    permission_classes = [IsAuthenticated]



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated] # По умолчанию требуем авторизацию

    # Переопределяем метод получения прав доступа
    def get_permissions(self):
        # Если действие - создание (регистрация), разрешаем всем
        if self.action == 'create':
            return [AllowAny()]
        # Для остальных действий (list, retrieve, update, destroy) - только авторизованным
        return super().get_permissions()

    # Используем разные сериализаторы для регистрации и остальных действий
    def get_serializer_class(self):
        if self.action == 'create':
            return StudentRegisterSerializer
        return StudentSerializer


class CreateSubscriptionView(APIView):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        try:
            # 1. Вызываем сервис (передаем название и цену курса)
            stripe_data = create_stripe_checkout_session(course.title, course.price)

            # 2. Создаем запись в вашей модели Payment
            payment = Payment.objects.create(
                user=request.user,
                study_course=course,  # Привязываем курс
                payment_amount=course.price,  # Сумма
                payment_option="stripe",  # Способ оплаты
                date_payment=datetime.date.today(),  # Дата
                stripe_session_id=stripe_data['session_id'],
                payment_link=stripe_data['url'],
                is_paid=False
            )

            return Response({
                "payment_link": payment.payment_link
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckPaymentStatusView(APIView):
    def get(self, request, payment_id):
        # Находим конкретный платеж
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)

        # Если в базе уже стоит True, просто возвращаем результат
        if payment.is_paid:
            return Response({"status": "Оплачено", "is_paid": True})

        if payment.stripe_session_id:
            # Идем в Stripe и спрашиваем: "А сессия cs_test_... оплачена?"
            current_status = get_stripe_payment_status(payment.stripe_session_id)

            if current_status == 'paid':
                # Обновляем нашу базу! Теперь при следующей попытке
                # Уровень 1 (проверка в БД) не даст ему купить курс снова.
                payment.is_paid = True
                payment.save()
                return Response({"status": "Оплачено", "is_paid": True})

        return Response({"status": "Ожидает оплаты", "is_paid": False})