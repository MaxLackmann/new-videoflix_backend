from django.urls import path
from content.api.views import VideoListView, VideoDetailView, ViewQualityView

urlpatterns = [
    path('video/', VideoListView.as_view(), name='video-list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoDetailView.as_view(), name='video-manifest'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>', ViewQualityView.as_view(), name='video-segment'),
]
