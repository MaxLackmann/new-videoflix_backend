import pytest
from django.urls import reverse
from user.models import CustomerUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

pytestmark = pytest.mark.django_db
def test_activate_user(client):
    user = CustomerUser.objects.create_user(
        username="testuser", email="testuser@test.com", password="Test1234", is_active=False
    )
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    url = reverse('activate', kwargs={'uidb64': uid, 'token': token})

    response = client.get(url)
    user.refresh_from_db()
    assert response.status_code == 200
    assert user.is_active is True

@pytest.mark.django_db
def test_activate_user_with_invalid_token(client):
    user = CustomerUser.objects.create_user(
        username="testuser", email="testuser@test.com", password="Test1234", is_active=False
    )
    
    token = "invalid_token"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    url = reverse('activate', kwargs={'uidb64': uid, 'token': token})

    response = client.get(url)
    user.refresh_from_db()
    assert response.status_code == 400
    assert user.is_active is False

@pytest.mark.django_db
def test_user_already_activated(client):
    user = CustomerUser.objects.create_user(
        username="testuser", email="testuser@test.com", password="Test1234", is_active=True
    )
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    url = reverse('activate', kwargs={'uidb64': uid, 'token': token})

    response = client.get(url)
    user.refresh_from_db()
    assert response.status_code == 200
    assert response.data["detail"] == "Account already activated."