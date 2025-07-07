import pytest
from django.urls import reverse
from user.models import CustomerUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import mail

@pytest.mark.django_db
def test_password_reset_sends_email(client):
    user = CustomerUser.objects.create_user(
        username="testuser", email="testuser@test.com", password="test1234", is_active=True
    )

    url = reverse('password_reset')
    data = {'email': 'testuser@test.com'}

    response = client.post(url, data)
    assert response.status_code == 200
    assert response.data["detail"] == "An email has been sent to reset your password."
    assert len(mail.outbox) == 1

@pytest.mark.django_db
def test_password_reset_invalid_email(client):
    url = reverse('password_reset')
    data = {'email': 'invalid_email'}

    response = client.post(url, data)
    assert response.status_code == 400
    assert response.data["detail"] == "Invalid email address"
    assert len(mail.outbox) == 0