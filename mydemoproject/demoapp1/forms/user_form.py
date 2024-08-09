from demoapp1.models.user import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user = User.objects.create_user(
            phone_number=self.cleaned_data['phone_number'],
            email=self.cleaned_data['email'],
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            role='newuser'  # Default role, or we can pass as needed
        )
        if commit:
            user.save()
        return user

