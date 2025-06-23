from django.urls import path
from content.api.views import VideoListView, VideoDetailView

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
]
