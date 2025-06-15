from django.urls import path
from user.api.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]
