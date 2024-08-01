from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.validators import MinValueValidator
from ._helper.base_model import BaseModel
from .book import Book


class Inventory(BaseModel):
    inventory_id = models.AutoField(primary_key=True)
    total_books = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    book = models.OneToOneField(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.book_name}: {self.total_books} books available"

    @staticmethod
    def get_total_books(book_id):
        inventory = Inventory.objects.filter(book_id=book_id).first()
        if inventory:
            return True, inventory.total_books
        else:
            return False, "Book is not in the inventory."

    @classmethod
    def add_inventory(cls, book, total_books):
        if total_books < 0:
            return False

        inventory = cls(
            total_books=total_books,
            book=book
        )
        inventory.save()
        return True

    @classmethod
    def available_count(cls, book_id):
        from .borrowed_book import BorrowedBook
        status, data = cls.get_total_books(book_id)
        if not status:
            return False, data

        if data - BorrowedBook.get_borrowed_books_count(book_id) < 1:
            return False, "No available copies to borrow"
        return True, "Success"

