from rest_framework.serializers import ModelSerializer
from users.models import Payment

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__' # Или перечислите конкретные поля, например: ('id', 'date_payment', 'payment_amount', 'payment_option', 'course', 'lesson', 'user')