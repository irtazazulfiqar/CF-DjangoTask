from django.db import models
from django.core.validators import MinValueValidator
from ._helper.base_model import BaseModel
from .book import Book


class Inventory(BaseModel):
    inventory_id = models.AutoField(primary_key=True)
    # 0 bcoz we can have 0 books in inventory when all borrowed
    total_books = models.IntegerField(validators=[MinValueValidator(0)])
    book = models.OneToOneField(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.book_name}: {self.total_books} books available"
    
    @staticmethod
    def get_total_books(bk):
        return Inventory.get_all().get(book=bk).total_books
