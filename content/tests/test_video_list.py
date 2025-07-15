
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from user.models import CustomerUser
from content.models import Video
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_video_list_authenticated_returns_all_videos(tmpdir):
    """
    Given an authenticated user and two videos in the database, when the user requests a list of all videos, then a list of all videos is returned.
    """

    user = CustomerUser.objects.create_user(
        username="user@test.com", email="user@test.com", password="testtest", is_active=True
    )
    video1 = Video.objects.create(
        title="Titel 1",
        description="Beschreibung 1",
        category="Drama"
    )
    video2 = Video.objects.create(
        title="Titel 2",
        description="Beschreibung 2",
        category="Romance"
    )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client = APIClient()
    client.cookies['access_token'] = access_token

    url = reverse("video-list")
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 2
    for video in response.data:
        assert set(video) == {"id", "created_at", "title", "description", "thumbnail_url", "category"}
        assert video["title"] in ["Titel 1", "Titel 2"]

@pytest.mark.django_db
def test_video_list_unauthenticated_returns_401():
    """
    Given an unauthenticated user, when the user requests a list of all videos, then a 401 Unauthorized status code is returned.
    """

    client = APIClient()
    url = reverse("video-list")
    response = client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_video_list_authenticated_empty_list():
    """
    Given an authenticated user with no videos in the database, when the user requests a list of all videos, then an empty list is returned.
    """
    
    user = CustomerUser.objects.create_user(
        username="user2@test.com", email="user2@test.com", password="password123", is_active=True
    )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client = APIClient()
    client.cookies['access_token'] = access_token

    url = reverse("video-list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data == []