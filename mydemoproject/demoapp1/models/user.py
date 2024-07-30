from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from ._helper.base_model import BaseModel


class CustomUser(AbstractUser, BaseModel):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=45, unique=True,
                              validators=[validate_email])
    phone_number = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'  # unique id
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.phone_number

    @classmethod
    def by_email(cls, email):
        return cls.filter_objects(email=email).exists()

    @classmethod
    def add_user(cls, email, phone_number, password, **extra_fields):
        if cls.by_email(email):
            raise ValidationError('User already exists')

        # We have to put else otherwise it will give warning
        # of code unreachable
        else:
            """
            Instead of creating this object we can also call UserManager
            create user function but i dont know whether it is optimal 
            or not
            """
            user = cls(
                email=email,
                phone_number=phone_number,
                password=make_password(password),
                **extra_fields
            )

            user.save()
            return user

    @classmethod
    def login(cls, email, password):
        try:
            user = cls.objects.get(email=email)
            if check_password(password, user.password):
                return user
            else:
                raise ValidationError('Invalid credentials')
        except ObjectDoesNotExist:
            raise ValidationError('User does not exist')
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError(f'An unexpected error occurred: {str(e)}')
