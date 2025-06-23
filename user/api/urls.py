from django.urls import path
from user.api.views import (
    RegisterView, VerifyEmailView, LoginView,
    PasswordResetView, PasswordResetRequestView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', PasswordResetRequestView.as_view(), name='forgot-password'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
]
