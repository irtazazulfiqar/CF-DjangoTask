import ssl
import string

from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
import random
from demoapp1.forms.otp_verification_form import OTPVerificationForm

from demoapp1.models.user import User
from demoapp1.utils import send_email_with_context

User = get_user_model()

# Disable SSL verification for local development only
ssl._create_default_https_context = ssl._create_unverified_context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = OTPVerificationForm
    template_name = 'password_reset_confirm_otp.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = self.get_user_from_uid(self.kwargs['uidb64'])
        if user is None:
            return self.form_invalid(form)

        session_otp = self.request.session.get('otp')

        if form.cleaned_data['otp'] != session_otp:
            form.add_error('otp', 'Invalid OTP.')
            return self.form_invalid(form)

        new_password = form.cleaned_data['new_password']
        confirm_password = form.cleaned_data['confirm_password']

        if new_password != confirm_password:
            form.add_error('confirm_password', 'Passwords do not match.')
            return self.form_invalid(form)

        if new_password == confirm_password:
            user.set_password(new_password)
            user.role = 'user'

            # Remove user from all groups
            user.groups.clear()

            # Add user to the 'newuser' group
            newuser_group = Group.objects.get(name='user')
            user.groups.add(newuser_group)

            # Remove all permissions
            user.user_permissions.clear()

            # Add permissions for 'user' group
            for permission in newuser_group.permissions.all():
                user.user_permissions.add(permission)

            user.save()

        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        user = self.get_user_from_uid(kwargs['uidb64'])

        otp = self.generate_otp()
        self.send_otp_email(user, otp)

        request.session['otp'] = otp

        return super().get(request, *args, **kwargs)

    def generate_otp(self, length=6):
        """Generate a random OTP."""
        otp = str(random.choices(string.digits, k=length))
        return otp

    def send_otp_email(self, user, otp):
        email_subject = 'Your OTP for Password Reset'

        success = send_email_with_context(email_subject, user.email,
                                          'demoapp1/otp_email_template.html',
                                          {
                                              'username': user.username,
                                              'otp': otp,
                                          })
        return success

    def get_user_from_uid(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            return None

    def handle_no_user(self):
        return redirect('password_reset')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'demoapp1/signup_signin.html'
