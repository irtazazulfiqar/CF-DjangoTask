from django.core.management.base import BaseCommand
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from demoapp1.models.user import User


class Command(BaseCommand):
    help = 'Send password reset emails to users with the role of olduser.'

    def handle(self, *args, **kwargs):
        # Filter users with the role of 'olduser'
        old_users = User.objects.filter(role='olduser')

        for user in old_users:
            # Generate the token and uid
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.SITE_URL}{reverse('password_reset_confirm',
                                                       kwargs={'uidb64': uid, 
                                                               'token': token})}"

            # Render HTML content from template
            context = {
                'username': user.username,
                'reset_link': reset_link
            }
            html_content = render_to_string('demoapp1/'
                                            'password_reset_email.html', context)

            # Send email using Django's send_mail function
            subject = 'Password Reset Request'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email

            try:
                send_mail(
                    subject,
                    strip_tags(html_content),  # Plain text content for email clients that do not support HTML
                    from_email,
                    [to_email],
                    html_message=html_content
                )
                self.stdout.write(self.style.SUCCESS(f'Password reset '
                                                     f'email sent to {user.email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to send password '
                                                   f'reset email to {user.email}. Error: {e}'))
