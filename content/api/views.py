from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from content.models import Video
from content.api.serializers import VideoSerializer
from django.http import Http404
import os
from django.http import FileResponse

class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class VideoDetailView(APIView):
    def get(self, request, movie_id: int, resolution: str):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video nicht gefunden.")
        hls_dir = video.video_file.path.replace('.mp4', f'_{resolution}')
        manifest_path = os.path.join(hls_dir, 'index.m3u8')
        if not os.path.exists(manifest_path):
            raise Http404("HLS-Manifest nicht gefunden.")
        return FileResponse(open(manifest_path, "rb"), content_type="application/vnd.apple.mpegurl")

class ViewQualityView(APIView):
    def get(self, request, movie_id: int, resolution: str, segment: str):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video nicht gefunden.")
        hls_dir = video.video_file.path.replace('.mp4', f'_{resolution}')
        segment_path = os.path.join(hls_dir, segment)
        if not os.path.exists(segment_path):
            raise Http404("HLS-Segment nicht gefunden.")
        return FileResponse(open(segment_path, "rb"), content_type="video/MP2T")