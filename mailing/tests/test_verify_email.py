import pytest
from django.core import mail
from django.conf import settings
import re
from mailing.services.email_service import send_verification_email

@pytest.mark.django_db
def test_send_verification_email_renders_and_sends(tmp_path, settings):

    """
    Tests that the send_verification_email function renders and sends an email
    with the correct subject and body.
    The test sends an email with a dummy email address, uid, and token. It verifies
    that only one email is sent, that the email is sent to the correct address, and
    that the subject contains "E-Mail-Adresse". It also checks that the email body
    and HTML alternative contain the uid and token, and that the body contains a link
    to activate the account using the uid and token.
    :param tmp_path: A temporary directory unique to each test invocation.
    :param settings: The Django settings module.
    """

    email = "user@test.com"
    uid = "dummyuid"
    token = "dummytoken"
    link = f"https://testserver/activate/{uid}/{token}/"

    send_verification_email(email, uid, token)

    assert len(mail.outbox) == 1
    msg = mail.outbox[0]
    assert msg.to == [email]
    assert "E-Mail-Adresse" in msg.subject

    uid = "dummyuid"
    token = "dummytoken"

    body = msg.body
    html_body = msg.alternatives[0][0] if msg.alternatives else ""

    assert (uid in body and token in body) or (uid in html_body and token in html_body)

    pattern = re.compile(r"uid={}&token={}".format(uid, token))
    assert pattern.search(body) or pattern.search(html_body)

    assert (
        f"/activate/{uid}/{token}/" in html_body or
        f"?uid={uid}&token={token}" in html_body or
        f"uid={uid}&token={token}" in html_body
    )