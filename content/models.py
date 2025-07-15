from django.db import models

def thumbnail_upload_to(instance, filename):
    """
    Generate a path for the thumbnail upload.
    The path consists of 'thumbnails/', the category of the video (replacing spaces with underscores and converting to lower case)
    and the filename of the thumbnail.
    :param instance: The Video instance for which the thumbnail is being uploaded
    :param filename: The filename of the thumbnail
    :return: A string representing the path to which the thumbnail should be uploaded
    """
    
    category = instance.category.replace(" ", "_").lower() if instance.category else "uncategorized"
    return f"thumbnails/{category}/{filename}"

def video_upload_to(instance, filename):
    """
    Generate a path for the video upload.
    The path consists of 'videos/', the category of the video (replacing spaces with underscores and converting to lower case)
    and the filename of the video.
    :param instance: The Video instance for which the video is being uploaded
    :param filename: The filename of the video
    :return: A string representing the path to which the video should be uploaded
    """

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
    