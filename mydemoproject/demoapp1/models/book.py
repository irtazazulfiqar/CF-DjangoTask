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

    """
        we done need extra field but if we expand 
        our system and add some new attributes to
        this model we will not have to change 
        add_book function
    """

    @classmethod
    def check_book_existence(cls, b_name, aut_name):
        try:
            cls.get_all().get(book_name=b_name, author_name=aut_name)
            return True

        except ObjectDoesNotExist:
            return False

    @classmethod
    def add_book(cls, b_name, aut_name, **extra_fields):

        if not cls.check_book_existence(b_name, aut_name):
            book = cls(
                book_name=b_name,
                author_name=aut_name,
                **extra_fields
            )
            book.save()
            return True, book

        else:
            return False, ("Cant add book because it already exists "
                           "for that particular author name")
