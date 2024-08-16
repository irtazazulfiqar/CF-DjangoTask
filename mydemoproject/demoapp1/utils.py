from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(subject, to_email, string_to_send):
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject,
            strip_tags(string_to_send),
            from_email,
            [to_email],
            html_message=string_to_send
        )
        return True
    except Exception as e:
        return False


def send_email_with_context(subject, to_email, template_name, context):
    html_content = render_to_string(template_name, context)
    email_sent = send_email(subject, to_email, html_content)

    return email_sent
