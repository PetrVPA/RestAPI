from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from users.serializers import PaymentSerializer  # Убедитесь, что он существует


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