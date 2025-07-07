import pytest
from django.urls import reverse
from user.models import CustomerUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

@pytest.mark.django_db
def test_password_reset(client):
    user = CustomerUser.objects.create_user(
        username="testuser", email="testuser@test.com", password="test1234", is_active=True
    )

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = str(RefreshToken.for_user(user))
    url = reverse('password_confirm', kwargs={'uidb64': uid, 'token': token})

    url = reverse('password_confirm', kwargs={'uidb64': uid, 'token': token})
    data = {'new_password': 'test4321', 'confirm_password': 'test4321'}

    response = client.post(url, data)
    assert response.status_code == 200
    assert response.data["detail"] == "Your Password has been successfully reset."

    user.refresh_from_db()
    assert user.check_password('test4321')

@pytest.mark.django_db
def test_password_reset_with_invalid_token(client):
    url = reverse('password_confirm', kwargs={'uidb64': 'invalid_token', 'token': 'invalid_token'})
    data = {'new_password': 'test4321', 'confirm_password': 'test4321'}

    response = client.post(url, data)
    assert response.status_code == 400
    assert response.data["detail"] == "Invalid token or user"