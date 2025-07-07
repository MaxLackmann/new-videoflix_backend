import pytest
from django.urls import reverse
from user.models import CustomerUser
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_logout_user(client):
    user = CustomerUser.objects.create_user(
        username="testuser", email="testuser@test.com", password="test1234", is_active=True
    )

    refreshtoken = RefreshToken.for_user(user)
    access_token = str(refreshtoken.access_token)

    client.cookies['access_token'] = access_token
    client.cookies['refresh_token'] = str(refreshtoken)

    url = reverse('logout')
    response = client.post(url)

    assert response.status_code == 200
    assert 'access_token' in response.cookies
    assert response.cookies['access_token'].value == ''
    assert 'refresh_token' in response.cookies
    assert response.cookies['refresh_token'].value == ''
    assert response.data["detail"] == "Logout successful"

@pytest.mark.django_db
def test_logout_user_no_refresh_token(client):
    url = reverse('logout')

    response = client.post(url)
    assert response.status_code == 400
    assert response.data["detail"] == "Refresh token not found"