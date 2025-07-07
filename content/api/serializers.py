from rest_framework import serializers
from content.models import Video

class VideoSerializer(serializers.ModelSerializer):
    url_120p = serializers.SerializerMethodField()
    url_240p = serializers.SerializerMethodField()
    url_360p = serializers.SerializerMethodField()
    url_480p = serializers.SerializerMethodField()
    url_720p = serializers.SerializerMethodField()
    url_1080p = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'date', 'video_file',
            'url_120p', 'url_240p', 'url_360p', 'url_480p', 'url_720p', 'url_1080p'
        ]

    def get_url_120p(self, obj):
        request = self.context.get('request')
        if obj.video_file and request:
            url = obj.video_file.url.replace(".mp4", "_120p.mp4")
            return request.build_absolute_uri(url)
        return None

    def get_url_240p(self, obj):
        request = self.context.get('request')
        if obj.video_file and request:
            url = obj.video_file.url.replace(".mp4", "_240p.mp4")
            return request.build_absolute_uri(url)
        return None
    
    def get_url_360p(self, obj):
        request = self.context.get('request')
        if obj.video_file and request:
            return request.build_absolute_uri(obj.video_file.url)
        return None


    def get_url_480p(self, obj):
        request = self.context.get('request')
        if obj.video_file and request:
            url = obj.video_file.url.replace(".mp4", "_480p.mp4")
            return request.build_absolute_uri(url)
        return None

    def get_url_720p(self, obj):
        request = self.context.get('request')
        if obj.video_file and request:
            url = obj.video_file.url.replace(".mp4", "_720p.mp4")
            return request.build_absolute_uri(url)
        return None

    def get_url_1080p(self, obj):
        request = self.context.get('request')
        if obj.video_file and request:
            url = obj.video_file.url.replace(".mp4", "_1080p.mp4")
            return request.build_absolute_uri(url)
        return None