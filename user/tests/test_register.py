import pytest
from django.urls import reverse
from user.models import CustomerUser

@pytest.mark.django_db
def test_register_user(client):
    url = reverse('register')
    data = {
        'email': "testuser@test.com",
        'password': "test1234",
        'confirmed_password': "test1234",
        'privacy_policy': 'on'
    }

    response = client.post(url, data)
    assert response.status_code == 201
    assert "user" in response.data
    assert "token" in response.data
    user = CustomerUser.objects.get(email="testuser@test.com")
    assert user.is_active is False

@pytest.mark.django_db
def test_register_user_with_existing_email(client):
    user = CustomerUser.objects.create_user(
        username="testuser", email="testuser@test.com", password="test1234"
    )
    url = reverse('register')
    data = {
        'email': "testuser@test.com",
        'password': "test1234",
        'confirmed_password': "test1234"
    }

    response = client.post(url, data)
    assert response.status_code == 400
    assert user.is_active is False

@pytest.mark.django_db
def test_register_user_passwords_not_matching(client):
    url = reverse('register')
    data = {
        'email': "testuser@test.com",
        'password': "test1234",
        'confirmed_password': "test12345",
    }

    response = client.post(url, data)
    assert response.status_code == 400
    assert response.data["detail"] == "Invalid email or password"

@pytest.mark.django_db
def test_superuser_is_active():
    user = CustomerUser.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
    assert user.is_active is True
    assert user.is_superuser is True
    assert user.is_staff is True

@pytest.mark.django_db
def test_normal_user_is_inactive():
    user = CustomerUser.objects.create_user(username='test', email='test@example.com', password='pass')
    assert user.is_active is False
    assert user.is_superuser is False
    assert user.is_staff is False