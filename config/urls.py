
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.serializers import CustomTokenObtainPairSerializer

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('study.urls', namespace='study')),
    path('student/', include('users.urls', namespace='users')),
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
