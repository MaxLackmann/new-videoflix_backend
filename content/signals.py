from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from content.models import Video
from content.tasks import (
    convert_480p,
    convert_720p,
    convert_1080p
)
import os
import shutil


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    After a Video object is saved, check if it is a new instance.
    If yes, and if the Video object has a video_file, start the transcoding
    process for all resolutions (480p, 720p, 1080p) in the background.
    """

    print('Video is saved')
    if created and instance.video_file:
        print('new Video is created')
        source = instance.video_file.path
        convert_480p.delay(source)
        convert_720p.delay(source)
        convert_1080p.delay(source)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Automatically delete the video file from filesystem
    when the corresponding `Video` object is deleted.
    Also deletes the HLS directories for all resolutions.
    """

    print('Video is deleted')
    if not instance.video_file:
        return

    base_path = instance.video_file.path
    if os.path.isfile(base_path):
        os.remove(base_path)
        print(f"Gelöscht: {base_path}")
    else:
        print(f"Nicht gefunden: {base_path}")

    hls_base = base_path.rsplit(".mp4", 1)[0]
    for res in ["480p", "720p", "1080p"]:
        dir_path = f"{hls_base}_{res}"
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
            print(f"Gelöscht: {dir_path}/")
        else:
            print(f"Nicht gefunden: {dir_path}/")
