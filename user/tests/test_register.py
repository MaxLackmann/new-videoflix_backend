import pytest
from django.urls import reverse
from user.models import CustomerUser

@pytest.mark.django_db
def test_register_user(client):
    url = reverse('register')
    data = {
        'email': "testuser@test.com",
        'password': "test1234",
        'repeated_password': "test1234"
    }

    response = client.post(url, data)
    assert response.status_code == 201
    assert "user" in response.data
    assert "token" in response.data
    user = CustomerUser.objects.get(email="testuser@test.com")
    assert user.is_active is False

@pytest.mark.django_db
def test_register_user_with_existing_email(client):
    CustomerUser.objects.create_user(
        username="testuser", email="testuser@test.com", password="test1234"
    )
    url = reverse('register')
    data = {
        'email': "testuser@test.com",
        'password': "test1234",
        'repeated_password': "test1234"
    }

    response = client.post(url, data)
    assert response.status_code == 400
    user = CustomerUser.objects.get(email="testuser@test.com")
    assert user.is_active is False

@pytest.mark.django_db
def test_register_user_passwords_not_matching(client):
    url = reverse('register')
    data = {
        'email': "testuser@test.com",
        'password': "test1234",
        'repeated_password': "test12345"
    }

    response = client.post(url, data)
    assert response.status_code == 400
    assert "detail" in response.data