from django.urls import path
from .views import CustomTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('me/', MeView.as_view(), name='auth-me'),
]
