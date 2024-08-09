from django.views.generic import (ListView, DeleteView,
                                  UpdateView)
from django.urls import reverse_lazy
from demoapp1.models.user import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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

