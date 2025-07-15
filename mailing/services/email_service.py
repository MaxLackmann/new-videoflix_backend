from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(email: str, uid: str, token: str) -> None:
    """Sends an email to the given address with a link to verify it.
    The email contains a link with a uid and token that can be used to
    verify the email address. The link is valid for 24 hours.
    Args:
        email (str): The email address to send the email to.
        uid (str): The uid of the user to verify.
        token (str): The token to verify the user.
    """
    
    subject = 'Bestätige deine E-Mail-Adresse'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    link = f'http://localhost:5500/pages/auth/activate.html?uid={uid}&token={token}'

    plain_message = (
        'Hallo!\n\n'
        'Bitte bestätige deine E-Mail-Adresse, indem du folgenden Link in deinen Browser kopierst:\n\n'
        f'{link}\n\n'
        'Der Link ist 24 Stunden gültig.\n\n'
        'Danke,\nDein Videoflix-Team'
    )

    html_message = render_to_string('verify_email.html', {'link': link})

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

def send_password_reset_email(email: str, uid: str, token: str) -> None:
    """Sends an email to the given address with a link to reset the password.
    The email contains a link with a uid and token that can be used to
    reset the password. The link is valid for 24 hours.
    Args:
        email (str): The email address to send the email to.
        uid (str): The uid of the user to reset the password.
        token (str): The token to reset the password.
    """
    
    subject = 'Setze dein Passwort zurück'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    link = f'http://localhost:5500/pages/auth/confirm_password.html?uid={uid}&token={token}'

    plain_message = (
        'Hallo!\n\n'
        'Du hast eine Rücksetzung deines Passworts angefordert.\n\n'
        'Um dein Passwort zurückzusetzen, kopiere folgenden Link in deinen Browser:\n\n'
        f'{link}\n\n'
        'Der Link ist 24 Stunden gültig.\n\n'
        'Danke,\nDein Videoflix-Team'
    )

    html_message = render_to_string('reset_password.html', {'link': link})

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )


