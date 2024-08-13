from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (ListView, DeleteView,
                                  UpdateView, CreateView)
from django.urls import reverse_lazy
from demoapp1.models.user import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import IntegrityError


class UserListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = 'demoapp1/users.html'
    context_object_name = 'users'
    permission_required = 'demoapp1.view_borrowedbook'


# DeleteView for Users
class UserDeleteView(PermissionRequiredMixin, DeleteView, LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('show_user')
    pk_url_kwarg = 'user_id'
    permission_required = 'demoapp1.view_borrowedbook'


# UpdateView for User
class UserUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'demoapp1/edit_form.html'
    context_object_name = 'user'
    success_url = reverse_lazy('show_user')
    pk_url_kwarg = 'user_id'
    permission_required = 'demoapp1.view_borrowedbook'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        # Check if email exists for another user
        if User.objects.filter(email=email):
            form.add_error('email', 'A user with this email already exists.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'User'
        context['edit_url'] = 'edit_user'
        return context


# we need to write this view to add user from admin panel


class UserAddView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = User
    template_name = 'demoapp1/users.html'
    fields = ['username', 'email', 'phone_number']
    permission_required = 'demoapp1.add_user'
    success_url = reverse_lazy('show_user')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']

        # Check if a user with the same email or phone number already exists
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'A user with this email already exists.')
            return self.form_invalid(form)

        if User.objects.filter(phone_number=phone_number).exists():
            form.add_error('phone_number', 'A user with this phone number already exists.')
            return self.form_invalid(form)

        # Generate a random password
        password = self._generate_random_password()

        try:
            success, result = User.add_user(
                email=email,
                phone_number=phone_number,
                password=password,
                username=form.cleaned_data['username'],
                role="user"
            )

            if success:
                # Optionally send the password to the user via email
                messages.success(self.request, 'User created successfully.')
                return redirect(self.success_url)  # Redirect after successful creation

                # return super().form_valid(form)
                # return redirect(self.success_url)
            else:
                form.add_error(None, result)
                return self.form_invalid(form)

        except IntegrityError:
            form.add_error(None, 'An unexpected error occurred. Please try again.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error creating user.')
        return super().form_invalid(form)

    def _generate_random_password(self):
        import random
        import string
        length = 8
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
