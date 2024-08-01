
from .inventory import Inventory
from django.db import models
from django.utils import timezone
from ._helper.base_model import BaseModel
from .user import CustomUser
from .book import Book


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
    borrow_dttm = models.DateTimeField(default=timezone.now)
    return_dttm = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name}"

    @classmethod
    def can_borrow_book(cls, user_id, book_id):
        if cls.objects.filter(user_id=user_id, book_id=book_id,
                              return_dttm__isnull=True).exists():
            return False, "Can't borrow book, Return previous one."

        return True, "Book can be borrowed"

    @classmethod
    def add_borrowed_book(cls, user, book):
        available, message = Inventory.available_count(book)
        if not available:
            return False, message

        can_borrow, message = cls.can_borrow_book(user, book)
        if not can_borrow:
            return False, message

        borrowed_book = cls(
            user=user,
            book=book,
            borrow_dttm=timezone.now(),
        )
        borrowed_book.save()

        return True, "Added Successfully"

    @classmethod
    def get_borrowed_books(cls, book_id):
        return cls.objects.filter(book_id=book_id,
                                  return_dttm__isnull=True).count()

    @classmethod
    def return_borrowed_book(cls, user, book):
        borrowed_book = cls.objects.filter(user=user, book=book,
                                           return_dttm__isnull=True).first()
        if not borrowed_book:
            return False, "No borrowed book found for this user."

        borrowed_book.return_dttm = timezone.now()
        borrowed_book.save()
        return True, "Book returned successfully."
