from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from user.api.views import (
    RegisterView, ActivateView, LoginView, LogoutView,
    TokenRefreshView, PasswordResetView, PasswordConfirmView
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_confirm/<uidb64>/<token>/', PasswordConfirmView.as_view(), name='password_confirm'),
]
