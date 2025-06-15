from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from content.models import Video
from content.tasks import (
    convert_120p,
    convert_480p,
    convert_720p,
    convert_1080p
)
import os


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video is saved')
    if created and instance.video_file:
        print('new Video is created')
        source = instance.video_file.path
        convert_120p.delay(source)
        convert_480p.delay(source)
        convert_720p.delay(source)
        convert_1080p.delay(source)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print('Video is deleted')

    if not instance.video_file:
        return

    base_path = instance.video_file.path
    variants = [
        base_path,
        base_path.replace(".mp4", "_120p.mp4"),
        base_path.replace(".mp4", "_480p.mp4"),
        base_path.replace(".mp4", "_720p.mp4"),
        base_path.replace(".mp4", "_1080p.mp4"),
    ]

    for file_path in variants:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f" Gelöscht: {file_path}")
        else:
            print(f" Nicht gefunden: {file_path}")
