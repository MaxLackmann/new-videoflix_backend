import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from user.models import CustomerUser
from content.models import Video
from rest_framework_simplejwt.tokens import RefreshToken
import os

@pytest.mark.django_db
def test_video_segment_success(settings):
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
        description="Segmenttest",
        category="Test",
        video_file=rel_video_path
    )

    client = APIClient()
    client.cookies['access_token'] = access_token

    hls_dir = os.path.join(video_dir, "Movie_480p")
    os.makedirs(hls_dir, exist_ok=True)
    segment_name = "segment_001.ts"
    segment_path = os.path.join(hls_dir, segment_name)
    with open(segment_path, "wb") as f:
        f.write(b"\x00\x01\x02dummyts")

    url = reverse("video-segment", kwargs={"movie_id": video.id, "resolution": "480p", "segment": segment_name})
    response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "video/MP2T"
    segment_body = b''.join(response.streaming_content)
    assert segment_body.startswith(b"\x00\x01\x02")

@pytest.mark.django_db
def test_video_segment_video_not_found(settings):
    """
    Existiert das Video nicht, wird 404 geliefert.
    """
    user = CustomerUser.objects.create_user(
        username="user@test.com", email="user@test.com", password="testtest", is_active=True
    )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client = APIClient()
    client.cookies['access_token'] = access_token

    url = reverse("video-segment", kwargs={"movie_id": 99999, "resolution": "480p", "segment": "segment_001.ts"})
    response = client.get(url)
    assert response.status_code == 404

