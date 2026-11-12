from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import PaymentViewSet, CreateSubscriptionView, CheckPaymentStatusView

app_name = 'users'

router = DefaultRouter()
router.register(r'payments', PaymentViewSet) # <--- Регистрируем наш ViewSet

urlpatterns = [
    path('', include(router.urls)),

    path('subscribe/<int:course_id>/', CreateSubscriptionView.as_view(), name='create_subscription'),
    path('payments/<int:payment_id>/check/', CheckPaymentStatusView.as_view(), name='check_payment'),

    path('', include(router.urls))
]