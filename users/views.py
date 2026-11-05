from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from users.serializers import PaymentSerializer  # Убедитесь, что он существует
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Student
from .serializers import StudentRegisterSerializer, StudentSerializer


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