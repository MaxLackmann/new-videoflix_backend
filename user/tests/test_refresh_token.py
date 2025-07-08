import pytest
from django.urls import reverse
from user.models import CustomerUser
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_refresh_token(client):
    user = CustomerUser.objects.create_user(
        username="testuser@test.com", email="testuser@test.com", password="test1234", is_active=True
    )

    refreshtoken = RefreshToken.for_user(user)
    client.cookies['refresh_token'] = str(refreshtoken)

    url = reverse('token_refresh')
    response = client.post(url)

    assert response.status_code == 200
    assert response.data["detail"] == "Token refreshed"
    assert 'access' in response.data
    assert 'access_token' in response.cookies
    assert response.cookies['access_token']['httponly'] is True

@pytest.mark.django_db
def test_no_refresh_token(client):
    url = reverse('token_refresh')
    response = client.post(url)
    assert response.status_code == 400
    assert response.data["detail"] == "Refresh token not found"

@pytest.mark.django_db
def test__invalid_refresh_token(client):
    client.cookies['refresh_token'] = "invalid_token"
    
    url = reverse('token_refresh')
    response = client.post(url)

    assert response.status_code == 401
    assert response.data["detail"] == "Invalid refresh token"