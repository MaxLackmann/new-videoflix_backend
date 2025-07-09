from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from content.models import Video
from content.api.serializers import VideoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class VideoListView(APIView):
    permission_classes = [JWTAuthentication]
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VideoDetailView(APIView):
    permission_classes = [JWTAuthentication]
    def get(self, request, pk):
        video = Video.objects.get(pk=pk)
        serializer = VideoSerializer(video, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
