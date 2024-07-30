from django.db import models
from ._helper.base_model import BaseModel
from django.utils import timezone
from .user import CustomUser
from .book import Book
from .inventory import Inventory


class BorrowedBook(BaseModel):
    """
    If a user is deleted, their associated borrowed book entries with a null return date
    must also be deleted. This is to prevent data inconsistency where a user has borrowed
    a book but never returned it. We don't want such entries in our database.
    """

    borrow_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name}"

    @classmethod
    def can_borrow_book(cls, user, book):
        if cls.get_all().filter(user=user, book=book,
                                return_date__isnull=True).exists():
            return False, ("You already have borrowed this book"
                           "previously and haven't returned it yet.")
        return True, "Book can be borrowed"

    @classmethod
    def add_borrowed_book(cls, user, book):

        available, message = Inventory.available_count(book)
        if not available:
            return False, message

        can_borrow, message = cls.can_borrow_book(user, book)
        if not can_borrow:
            return False, message

        # removed addEntry() and embedded it here
        borrowed_book = cls(
            user=user,
            book=book,
            borrow_date=timezone.now().date(),
        )
        borrowed_book.save()

        return True, "Added Successfully"

    @classmethod
    def get_borrowed_books(cls, book):
        return BorrowedBook.get_all().filter(book=book,
                                             return_date__isnull=True).count()
