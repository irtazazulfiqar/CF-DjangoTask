from django.core.management.base import BaseCommand
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from demoapp1.models.user import User
from django.conf import settings
from demoapp1.utils import send_email


class Command(BaseCommand):
    help = 'Send password reset emails to users with the previous user.'

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
            html_content = render_to_string(
                'demoapp1/password_reset_email.html', context)

            # Use the reusable send_email function, created a utils.py file
            success = send_email('Password Reset Request', user.email,
                                html_content)
            if success:
                self.stdout.write(self.style.SUCCESS(f'Password reset email sent '
                                                     f'to {user.email}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to send password '
                                                   f'reset email to {user.email}.'))


