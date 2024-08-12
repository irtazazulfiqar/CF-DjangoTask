import ssl
from django.core.management.base import BaseCommand
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from demoapp1.models.user import User
import sendgrid
from sendgrid.helpers.mail import Mail


class Command(BaseCommand):
    help = 'Send password reset emails to users with the role of olduser.'

    def handle(self, *args, **kwargs):
        # Filter users with the role of 'olduser'
        old_users = User.objects.filter(role='olduser')

        for user in old_users:
            # Generate the token and uid
            token = PasswordResetTokenGenerator().make_token(user)
            if user.email == 'irtazazulfiaar143@gmail.com':
                print(token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.SITE_URL}{reverse('password_reset_confirm',
                                                       kwargs={'uidb64': uid, 'token': token})}"

            # Email subject and content
            email_subject = 'Password Reset Request'

            # HTML content for the email
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Password Reset Request</title>
            </head>
            <body>
                <p>Dear {user.username},</p>
                <p>You have requested a password reset. Please click the link below to reset your password:</p>
                <p><a href="{reset_link}">Reset Password</a></p>
                <p>If you did not request a password reset, please ignore this email.</p>
                <p>Best regards,<br>
                Library Team</p>
                <p><img src="https://feji.us/ngrv2f" alt="Library Logo" style="width: 150px; height: auto;"></p>
            </body>
            </html>
            """

            # Send email using SendGrid
            sendgrid_client = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email

            mail = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=email_subject,
                html_content=html_content
            )

            # Disable SSL verification if needed
            ssl._create_default_https_context = ssl._create_unverified_context

            # Send the email
            # response = sendgrid_client.send(mail)
            try:
                response = sendgrid_client.send(mail)
                self.stdout.write(self.style.SUCCESS(f'Password reset email sent'
                                                     f' to {user.email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Password reset email sent'
                                                   f' to {user.email}'))
