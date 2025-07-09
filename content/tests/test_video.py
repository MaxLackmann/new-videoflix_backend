import pytest
from content.models import Video
from user.models import CustomerUser
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return CustomerUser.objects.create_user(
        username='test', email='test@example.com', password='test'
    )

@pytest.mark.django_db
def test_video_list_authenticated(api_client, user):
    api_client.force_authenticate(user=user)
    Video.objects.create(title="Test", description="Desc")
    url = reverse('video-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1

@pytest.mark.django_db
def test_video_list_empty(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('video-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data == []

@pytest.mark.django_db
def test_video_list_unauthorized(api_client):
    url = reverse('video-list')
    response = api_client.get(url)
    assert response.status_code == 401
