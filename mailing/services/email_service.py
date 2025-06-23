from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(email: str, token: str) -> None:
    subject = 'Bestätige deine E-Mail-Adresse'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    link = f'http://localhost:4200/verify-email?token={token}'

    plain_message = (
        'Hallo!\n\n'
        'Bitte bestätige deine E-Mail-Adresse, indem du folgenden Link in deinen Browser kopierst:\n\n'
        f'{link}\n\n'
        'Der Link ist 24 Stunden gültig.\n\n'
        'Danke,\nDein Videoflix-Team'
    )

    html_message = render_to_string('verify_email.html', {'token': token, 'link': link})

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_password_reset_email(email: str, token: str) -> None:
    subject = 'Setze dein Passwort zurück'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    link = f'http://localhost:4200/reset-password?token={token}'

    plain_message = (
        'Hallo!\n\n'
        'Du hast eine Rücksetzung deines Passworts angefordert.\n\n'
        'Um dein Passwort zurückzusetzen, kopiere folgenden Link in deinen Browser:\n\n'
        f'{link}\n\n'
        'Der Link ist 24 Stunden gültig.\n\n'
        'Danke,\nDein Videoflix-Team'
    )

    html_message = render_to_string('reset_password.html', {'token': token, 'link': link})

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )


