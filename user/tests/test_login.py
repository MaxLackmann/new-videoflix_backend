import pytest
from django.urls import reverse
from user.models import CustomerUser

@pytest.mark.django_db
def test_login_user(client):
    user = CustomerUser.objects.create_user(
        username="testuser@test.com", email="testuser@test.com", password="test1234", is_active=True
    )
    url = reverse('login')
    data = {'email': "testuser@test.com", 'password': "test1234"}
    response = client.post(url, data)

    assert response.status_code == 200
    assert user.is_active is True
    assert response.data["detail"] == "Login successful"

@pytest.mark.django_db
def test_login_inactive_user(client):
    user = CustomerUser.objects.create_user(
        username="testuser@test.com",
        email="testuser@test.com",
        password="test1234",
        is_active=False
    )
    
    data = {'email': "testuser@test.com", 'password': "test1234"}
    url = reverse('login')

    response = client.post(url, data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_login_user_with_invalid_password(client):
    CustomerUser.objects.create_user(
        username="testuser@test.com", email="testuser@test.com", password="test1234"
    )
    url = reverse('login')
    data = {'email': "testuser@test.com", 'password': "test12345"}

    response = client.post(url, data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_login_user_with_invalid_email(client):
    user = CustomerUser.objects.create_user(
        username="testuser@test.com", email="testuser@test.com", password="test1234"
    )
    url = reverse('login')
    data = {'email': "testuser2@test.com", 'password': "test1234"}

    response = client.post(url, data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_login_sets_jwt_cookies(client):
    user = CustomerUser.objects.create_user(
        username="testuser@test.com", email="testuser@test.com",
        password="test1234", is_active=True
    )
    url = reverse('login')
    data = {'email': 'testuser@test.com', 'password': 'test1234'}

    response = client.post(url, data)
    assert response.status_code == 200
    assert 'access_token' in response.cookies
    assert response.cookies['access_token']['httponly']
    assert 'refresh_token' in response.cookies
    assert response.cookies['refresh_token']['httponly']