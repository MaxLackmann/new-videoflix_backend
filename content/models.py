from django.db import models
from datetime import date

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(default=date.today)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
