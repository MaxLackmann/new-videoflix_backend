from django.urls import path
from content.api.views import VideoListView, VideoDetailView

urlpatterns = [
    path('video/', VideoListView.as_view(), name='video-list'),
    path('video/<int:movie_id>/', VideoDetailView.as_view(), name='video-detail'),
]
