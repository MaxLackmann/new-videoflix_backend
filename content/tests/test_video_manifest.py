import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from user.models import CustomerUser
from content.models import Video
from rest_framework_simplejwt.tokens import RefreshToken
import os

@pytest.mark.django_db
def test_video_manifest_success(settings):
    """
    Test that a video manifest is successfully retrieved with a 200 status code.
    This test creates a user and a dummy video file, along with an HLS manifest
    file. It then authenticates the user and makes a GET request to retrieve 
    the video manifest. The response is verified to have a 200 status code, 
    the correct content type for HLS manifests, and the body starts with the 
    expected '#EXTM3U' header.
    """

    user = CustomerUser.objects.create_user(
        username="user@test.com", email="user@test.com", password="testtest", is_active=True
    )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    media_root = settings.MEDIA_ROOT
    video_dir = os.path.join(media_root, "videos")
    os.makedirs(video_dir, exist_ok=True)
    video_path = os.path.join(video_dir, "Movie.mp4")
    with open(video_path, "w") as f:
        f.write("dummy video content")

    category = "Test"
    rel_video_path = os.path.relpath(video_path, media_root)
    video = Video.objects.create(
        title="Movie",
        description="Testmovie",
        category=category,
        video_file=rel_video_path
    )
    basename, _ = os.path.splitext(os.path.basename(video_path))
    hls_dir = os.path.join(video_dir, category.lower(), f"{basename}_480p")
    os.makedirs(hls_dir, exist_ok=True)
    manifest_path = os.path.join(hls_dir, "index.m3u8")
    with open(manifest_path, "w") as f:
        f.write("#EXTM3U\n#EXT-X-VERSION:3\n")

    client = APIClient()
    client.cookies['access_token'] = access_token

    url = reverse("video-manifest", kwargs={"movie_id": video.id, "resolution": "480p"})
    response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/vnd.apple.mpegurl"
    manifest_body = b''.join(response.streaming_content)
    assert manifest_body.startswith(b"#EXTM3U")


@pytest.mark.django_db
def test_video_manifest_video_not_found(settings):
    """
    Test that a 404 status code is returned when the video manifest is not found
    because the video with the given id does not exist.
    """
    
    user = CustomerUser.objects.create_user(
        username="user@test.com", email="user@test.com", password="testtest", is_active=True
    )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client = APIClient()
    client.cookies['access_token'] = access_token

    url = reverse("video-manifest", kwargs={"movie_id": 99999, "resolution": "480p"})
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_video_manifest_manifest_not_found(settings):
    """
    Test that a 404 status code is returned when the video manifest is not found
    because the manifest file does not exist, even though the video with the given
    id does exist.
    """

    user = CustomerUser.objects.create_user(
        username="user@test.com", email="user@test.com", password="testtest", is_active=True
    )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    media_root = settings.MEDIA_ROOT
    video_dir = os.path.join(media_root, "videos")
    os.makedirs(video_dir, exist_ok=True)
    video_path = os.path.join(video_dir, "Movie.mp4")
    with open(video_path, "w") as f:
        f.write("dummy video content")

    rel_video_path = os.path.relpath(video_path, media_root)
    video = Video.objects.create(
        title="Movie",
        description="Testmovie",
        category="Test",
        video_file=rel_video_path
    )

    client = APIClient()
    client.cookies['access_token'] = access_token

    hls_dir = os.path.join(video_dir, video.category.lower(), "Movie_480p")
    os.makedirs(hls_dir, exist_ok=True)

    manifest_path = os.path.join(hls_dir, "index.m3u8")
    if os.path.exists(manifest_path):
        os.remove(manifest_path)
    
    url = reverse("video-manifest", kwargs={"movie_id": video.id, "resolution": "480p"})
    response = client.get(url)
    assert response.status_code == 404