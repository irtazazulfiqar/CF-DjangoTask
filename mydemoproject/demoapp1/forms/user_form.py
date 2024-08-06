from demoapp1.models.user import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'password1', 'password2']


