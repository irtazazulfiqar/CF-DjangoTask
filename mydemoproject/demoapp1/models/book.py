from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from ._helper.base_model import BaseModel


class Book(BaseModel):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=45)
    author_name = models.CharField(max_length=45)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author_name', 'book_name'],
                                    name='unique_author_book')
        ]

    def __str__(self):
        return self.book_name

    @classmethod
    def check_book_existence(cls, book_name, auth_name):
        return cls.objects.filter(book_name=book_name, author_name=auth_name).exists()

    @classmethod
    def add_book(cls, b_name, aut_name, **extra_fields):
        """
            we do not need an extra field but if we expand
            our system and add some new attributes to
            this model, we will not have to change
            add_book function
        """

        if not cls.check_book_existence(b_name, aut_name):
            book = cls(
                book_name=b_name,
                author_name=aut_name,
                **extra_fields
            )
            book.save()
            return True, book

        else:
            return False, "Book already exists."
