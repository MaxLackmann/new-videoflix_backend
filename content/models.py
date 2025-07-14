from django.db import models

def thumbnail_upload_to(instance, filename):
    category = instance.category.replace(" ", "_").lower() if instance.category else "uncategorized"
    return f"thumbnails/{category}/{filename}"

def video_upload_to(instance, filename):
    category = instance.category.replace(" ", "_").lower() if instance.category else "uncategorized"
    return f"videos/{category}/{filename}"

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, default="", blank=True)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to, blank=True, null=True)
    video_file = models.FileField(upload_to=video_upload_to, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.title
    