from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email, MaxValueValidator


# abstract model
class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def filter_objects(cls, **kwargs):
        return cls.objects.filter(**kwargs)

    @classmethod
    def get_first(cls, **kwargs):
        return cls.objects.filter(**kwargs).first()


class CustomUser(AbstractUser, BaseModel):
    user_id = models.AutoField(primary_key=True,)
    email = models.EmailField(max_length=45, unique=True,
                              validators=[validate_email])
    phone_number = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    USERNAME_FIELD = 'phone_number'  # unique id
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.phone_number


class Book(BaseModel):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=45)
    author_name = models.CharField(max_length=45)

    def __str__(self):
        return self.book_name


class BorrowedBook(BaseModel):
    borrow_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name}"


class Inventory(BaseModel):
    id = models.AutoField(primary_key=True)
    total_books = models.IntegerField(validators=[MaxValueValidator(100)])
    book = models.OneToOneField(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.book_name}: {self.total_books} books available"
