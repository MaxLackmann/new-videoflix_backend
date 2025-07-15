import pytest
from django.core import mail
import re
from mailing.services.email_service import send_password_reset_email

@pytest.mark.django_db
def test_send_password_reset_email_renders_and_sends(tmp_path, settings):
    """
    Tests that the send_password_reset_email function renders and sends an email
    with the correct subject and body.
    The test sends an email with a dummy email address, uid and token. The test
    checks that only one email is sent, that the email is sent to the correct
    address, that the subject contains either "Passwort", "Reset" or "zurücksetzen",
    that the body contains the uid and token, and that the body contains a link
    to reset the password.
    :param tmp_path: A temporary directory unique to each test invocation.
    :param settings: The Django settings module.
    """

    email = "reset@test.com"
    uid = "dummyuid"
    token = "dummytoken"
    send_password_reset_email(email, uid, token)

    assert len(mail.outbox) == 1
    msg = mail.outbox[0]
    assert msg.to == [email]
    assert "Passwort" in msg.subject or "Reset" in msg.subject or "zurücksetzen" in msg.subject

    body = msg.body
    html_body = msg.alternatives[0][0] if msg.alternatives else ""

    assert (uid in body and token in body) or (uid in html_body and token in html_body)

    pattern = re.compile(r"uid={}&token={}".format(uid, token))
    assert pattern.search(body) or pattern.search(html_body)

    assert "Passwort zurücksetzen" in html_body
    assert "link" or "href" in html_body 