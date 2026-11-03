from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import PaymentViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'payments', PaymentViewSet) # <--- Регистрируем наш ViewSet

urlpatterns = [
    path('', include(router.urls)),
]