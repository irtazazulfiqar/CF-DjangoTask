from django.views.generic import (ListView, DeleteView,
                                  UpdateView)
from django.urls import reverse_lazy
from demoapp1.models.user import User
from django.contrib.auth.mixins import LoginRequiredMixin


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'demoapp1/users.html'
    context_object_name = 'users'


# DeleteView for Users
class UserDeleteView(DeleteView, LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('show_user')
    pk_url_kwarg = 'user_id'


# UpdateView for User
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'demoapp1/edit_form.html'
    context_object_name = 'user'
    success_url = reverse_lazy('show_user')
    pk_url_kwarg = 'user_id'

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

