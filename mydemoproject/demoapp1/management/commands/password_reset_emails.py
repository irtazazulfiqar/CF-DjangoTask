from django.core.management.base import BaseCommand
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from demoapp1.models.user import User
from demoapp1.utils import send_email_with_context
from datetime import datetime
from django.utils import timezone


class Command(BaseCommand):
    help = ('Send password reset emails to users with the role "user" '
            'whose account was created before the provided date and time.')

    def add_arguments(self, parser):
        parser.add_argument('datetime', type=str, help='Date and time in the'
                                                       ' format "YYYY-MM-DD '
                                                       'HH:MM:SS"')

    def handle(self, *args, **kwargs):
        # Get the input date and time
        input_datetime_str = kwargs['datetime']

        # Parse the datetime input
        try:
            input_datetime = datetime.strptime(input_datetime_str,
                                               '%Y-%m-%d %H:%M:%S')
            # Convert to timezone-aware datetime using Django's timezone
            input_datetime = timezone.make_aware(input_datetime,
                                                 timezone.get_current_timezone())
        except ValueError:
            self.stdout.write(self.style.ERROR('Invalid datetime format. '
                                               'Please use "YYYY-MM-DD HH:MM:SS".'))
            return

        # Filter users with the role of 'user' and created before the input datetime
        old_users = User.objects.filter(role='user',
                                        created_at__lt=input_datetime)

        if not old_users.exists():
            self.stdout.write(
                self.style.WARNING('No users found with the role "user" '
                                   'created before the specified datetime.'))
            return
        # Send password reset emails
        for user in old_users:
            # Generate the token and uid
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = f"{settings.SITE_URL}{reverse(
                'password_reset_confirm',
                kwargs={'uidb64': uid, 'token': token})}"

            # Render HTML content from template
            context = {
                'username': user.username,
                'reset_link': reset_link
            }

            success = send_email_with_context("Create Your Account", user.email,
                                              'demoapp1/password_reset_email.html',
                                              context)

            if success:
                self.stdout.write(self.style.SUCCESS(f'Password reset email '
                                                     f'sent to {user.email}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to send password '
                                                   f'reset email to {user.email}'))
