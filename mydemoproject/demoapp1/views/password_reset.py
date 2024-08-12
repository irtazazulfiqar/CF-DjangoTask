import ssl
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
import random
from demoapp1.forms.otp_verification_form import OTPVerificationForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from demoapp1.models.user import User

User = get_user_model()

# Disable SSL verification for local development only
ssl._create_default_https_context = ssl._create_unverified_context
import logging


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = OTPVerificationForm
    template_name = 'password_reset_confirm_otp.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = self.get_user_from_uid(self.kwargs['uidb64'])
        session_otp = self.request.session.get('otp')
        token = self.kwargs.get('token')

        if form.cleaned_data['otp'] == session_otp:
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password == confirm_password:
                user.set_password(new_password)
                user.role = 'newuser'

                # Remove user from all groups
                user.groups.clear()

                # Add user to the 'newuser' group
                newuser_group = Group.objects.get(name='newuser')
                user.groups.add(newuser_group)

                # Remove all permissions
                user.user_permissions.clear()

                # Add permissions for 'newuser' group
                for permission in newuser_group.permissions.all():
                    user.user_permissions.add(permission)

                user.save()
                return redirect(self.success_url)
            else:
                form.add_error('confirm_password', 'Passwords do not match.')
        else:
            form.add_error('otp', 'Invalid OTP.')

        return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        user = self.get_user_from_uid(kwargs['uidb64'])

        otp = self.generate_otp()
        self.send_otp_email(user, otp)

        request.session['otp'] = otp

        return super().get(request, *args, **kwargs)

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_otp_email(self, user, otp):
        email_subject = 'Your OTP for Password Reset'

        # Load and render the HTML template
        html_content = render_to_string(
            'demoapp1/otp_email_template.html', {
                'username': user.username,
                'otp': otp,
            })

        # Create the plain text version of the email
        plain_text_content = strip_tags(html_content)

        # Send the email using Django’s send_mail function

        send_mail(
            subject=email_subject,
            message=plain_text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_content
        )


    def get_user_from_uid(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            logging.debug(f"User retrieved in get_user_from_uid: {user}")
            return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            logging.debug(f"Error retrieving user from uid: {e}")
            return None

    def handle_no_user(self):
        return redirect('password_reset')
