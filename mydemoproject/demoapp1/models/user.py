from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from ._helper.base_model import BaseModel
from ._helper.time_stamp import TimeStampedModel
from demoapp1.manager import UserManager


class User(AbstractUser, BaseModel, TimeStampedModel):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=45, unique=True,
                              validators=[validate_email])
    phone_number = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'email'  # unique id
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    @classmethod
    def by_email(cls, email):
        return cls.objects.filter(email=email).exists()

    @classmethod
    def by_phone(cls, phone_number):
        return cls.objects.filter(phone_number=phone_number).exists()

    @classmethod
    def add_user(cls, email, phone_number, password, **extra_fields):
        if cls.by_email(email):
            return False, "User already exists"
        if cls.by_phone(phone_number):
            return False, "Phone-number already registered"

        """
        Instead of creating this object we can also call UserManager
        create user function but i dont know whether it is optimal 
        or not.
        """
        user = cls(
                email=email,
                phone_number=phone_number,
                password=make_password(password),
                **extra_fields
        )

        user.save()
        return True, user

    @classmethod
    def login(cls, email, password):
        user = cls.objects.filter(email=email).first()

        if not user:
            return False, "User does not exist"

        if not check_password(password, user.password):
            return False, "Invalid credentials"

        return True, "Valid Credentials"
