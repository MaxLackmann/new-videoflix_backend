from django.urls import path, include

urlpatterns = [
    path('', include('user.api.urls')),
    path('', include('content.api.urls')),
]
