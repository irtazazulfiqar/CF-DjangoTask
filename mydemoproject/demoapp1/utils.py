from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags


def send_email(subject, to_email, html_content):
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject,
            strip_tags(html_content),
            from_email,
            [to_email],
            html_message=html_content
        )
        return True
    except Exception as e:
        return False