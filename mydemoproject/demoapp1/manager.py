from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None, role='newuser', **extra_fields):
        if not phone_number:
            raise ValueError('The Phone number must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, role=role, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        # Remove all direct permissions from the user
        user.user_permissions.clear()

        # Assign group based on role
        if role == 'admin':
            print("Role assigned to admmin")

            group = Group.objects.get(name='admin')
        elif role == 'olduser':
            group = Group.objects.get(name='olduser')
        else:
            print("Role assigned to newusers")
            group = Group.objects.get(name='newuser')

        user.groups.add(group)
        user.save()

        return user

    def create_superuser(self, phone_number, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, email=email, username=username, password=password, **extra_fields)
