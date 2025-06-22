from django.urls import path, include

urlpatterns = [
    path('userapp/', include('user.api.urls')),
    # path('contentapp/', include('content.api.urls')),
    # path('mailingapp/', include('mailing.api.urls')),
]
