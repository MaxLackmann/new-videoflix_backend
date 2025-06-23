from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from content.models import Video
from content.api.serializers import VideoSerializer

class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VideoDetailView(APIView):
    def get(self, request, pk):
        video = Video.objects.get(pk=pk)
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)
