from rest_framework import serializers
from content.models import Video

class VideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = [
            'id',
            'created_at',
            'title',
            'description',
            'category',
            'thumbnail_url',
        ]
        read_only_fields = fields

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            return request.build_absolute_uri(obj.thumbnail.url) if request else obj.thumbnail.url
        return None