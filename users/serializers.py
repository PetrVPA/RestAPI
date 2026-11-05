from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import Payment, Student


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__' # Или перечислите конкретные поля, например: ('id', 'date_payment', 'payment_amount', 'payment_option', 'course', 'lesson', 'user')


# Для регистрации (создания пользователя)
class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ('email', 'password', 'phone', 'city', 'avatar')

    def create(self, validated_data):
        # Используем create_user, чтобы пароль захешировался
        user = Student.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            city=validated_data.get('city', ''),
            avatar=validated_data.get('avatar', None)
        )
        return user

# Для CRUD операций над пользователями
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__' # Или перечислите конкретные поля, исключив пароль