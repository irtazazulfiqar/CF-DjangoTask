from django.contrib import admin
from .models.inventory import Inventory, Book
from .models.borrowed_book import BorrowedBook
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('username',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_name', 'author_name')
    search_fields = ('book_name', 'author_name')
    list_filter = ('author_name',)


class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('borrow_id', 'user', 'book', 'borrow_dttm', 'return_dttm')
    search_fields = ('user__username', 'book__book_name')
    list_filter = ('borrow_dttm', 'return_dttm')
    autocomplete_fields = ['user', 'book']
    ordering = ('-borrow_dttm',)



class InventoryAdmin(admin.ModelAdmin):
    list_display = ('inventory_id', 'book', 'total_books')
    search_fields = ('book__book_name',)
    list_filter = ('total_books',)


admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowedBook, BorrowedBookAdmin)
admin.site.register(Inventory, InventoryAdmin)
