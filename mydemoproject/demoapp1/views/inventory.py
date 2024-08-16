from django.views.generic import ListView
from demoapp1.models.book import Book
from demoapp1.models.inventory import Inventory
from demoapp1.models.user import User
from demoapp1.models.borrowed_book import BorrowedBook
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# ListView for Inventory
class InventoryListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Inventory
    template_name = 'demoapp1/inventory.html'
    context_object_name = 'inventory_with_borrowed'
    permission_required = 'demoapp1.view_inventory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory_items = Inventory.objects.all()
        inventory_with_borrowed = []

        for inventory_item in inventory_items:
            borrowed_count = (BorrowedBook.
                              get_borrowed_books_count(inventory_item.book.book_id))
            inventory_with_borrowed.append({
                'inventory': inventory_item,
                'borrowed_count': borrowed_count
            })

        context['inventory_with_borrowed'] = inventory_with_borrowed
        context['users'] = User.objects.all()
        context['books'] = Book.objects.all()
        return context

