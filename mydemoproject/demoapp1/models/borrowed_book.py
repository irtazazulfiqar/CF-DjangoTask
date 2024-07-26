from django.db import models
from ._helper.base_model import BaseModel
from django.utils import timezone
from .user import CustomUser
from .book import Book
from .inventory import Inventory


class BorrowedBook(BaseModel):
    """
        if user is deleted then its associated entries must also be deleted
        I.E only those whose return dates are null
        because of data inconsistency, what if user borrowed a book and never
        returned it, we don't want these kind of entries in our db
    """

    borrow_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)

    @classmethod
    def can_borrow_book(cls, user, book):
        if cls.get_all().filter(user=user, book=book,
                                return_date__isnull=True).exists():
            return False, ("Book can't be borrowed, you already "
                           "haven't returned the previous one")
        return True, "Book can be borrowed"

    @classmethod
    def add_entry(cls, user, book):

        borrowed_book = cls(
            user=user,
            book=book,
            borrow_date=timezone.now().date(),
        )
        borrowed_book.save()
        return True, borrowed_book

    @classmethod
    def add_borrowed_book(cls, user, book):

        if Inventory.get_total_books(book) - cls.get_borrowed_books(book) <= 0:
            return False, "No available copies to borrow"

        can_borrow, message = cls.can_borrow_book(user, book)
        if not can_borrow:
            return False, message

        success, result = cls.add_entry(user, book)

        return success, result

    @classmethod
    def get_borrowed_books(cls, book):
        return BorrowedBook.get_all().filter(book=book,
                                             return_date__isnull=True).count()

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name}"
