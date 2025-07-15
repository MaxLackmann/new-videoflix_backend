from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from content.models import Video
from content.api.serializers import VideoSerializer
from django.http import Http404
import os
from django.http import FileResponse
from django.conf import settings

class VideoListView(APIView):
    def get(self, request):
        """
        Get a list of all videos.
        Returns a list of all Video objects, serialized with VideoSerializer.
        :param request: The request object
        :return: A Response object with the list of videos
        """

        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoDetailView(APIView):
    def get(self, request, movie_id: int, resolution: str):
        """
        Retrieve the HLS manifest file for a specific video and resolution.
        This method attempts to find and return the HLS manifest file for the specified 
        movie ID and resolution. If the video with the given ID does not exist, or if 
        the manifest file is not found, an HTTP 404 error is raised.
        :param request: The request object
        :param movie_id: The ID of the video to retrieve
        :param resolution: The resolution of the video (e.g., "480p", "720p")
        :return: A FileResponse with the HLS manifest content
        :raises Http404: If the video or HLS manifest cannot be found
        """

        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video nicht gefunden.")

        media_root = settings.MEDIA_ROOT
        category = video.category.lower()
        basename, _ = os.path.splitext(os.path.basename(video.video_file.name))
        hls_dir = os.path.join(media_root, "videos", category, f"{basename}_{resolution}")
        manifest_path = os.path.join(hls_dir, "index.m3u8")
        if not os.path.isfile(manifest_path):
            raise Http404("HLS-Manifest nicht gefunden.")
        return FileResponse(open(manifest_path, "rb"), content_type="application/vnd.apple.mpegurl")

class ViewQualityView(APIView):
    def get(self, request, movie_id: int, resolution: str, segment: str):
        """
        Retrieve a single video segment from an HLS manifest file.
        This method attempts to find and return the HLS segment file for the specified 
        movie ID, resolution, and segment name. If the video with the given ID does not exist, 
        or if the segment file is not found, an HTTP 404 error is raised.
        :param request: The request object
        :param movie_id: The ID of the video to retrieve
        :param resolution: The resolution of the video (e.g., "480p", "720p")
        :param segment: The name of the segment file to retrieve
        :return: A FileResponse with the HLS segment content
        :raises Http404: If the video or HLS segment cannot be found
        """
        
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video nicht gefunden.")

        media_root = settings.MEDIA_ROOT
        category = video.category.lower()
        basename, _ = os.path.splitext(os.path.basename(video.video_file.name))
        hls_dir = os.path.join(media_root, "videos", category, f"{basename}_{resolution}")
        segment_path = os.path.join(hls_dir, segment)
        if not os.path.isfile(segment_path):
            raise Http404("HLS-Segment nicht gefunden.")
        return FileResponse(open(segment_path, "rb"), content_type="video/MP2T")