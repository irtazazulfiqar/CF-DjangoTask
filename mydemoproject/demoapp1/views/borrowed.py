from django.contrib import messages
from django.shortcuts import redirect
from django.utils.dateparse import parse_date
from django.views.generic import ListView, TemplateView
from demoapp1.models.book import Book
from demoapp1.models.inventory import Inventory
from demoapp1.models.user import User
from demoapp1.models.borrowed_book import BorrowedBook
from django.contrib.auth.mixins import LoginRequiredMixin


class BorrowReturnView(TemplateView):
    template_name = 'demoapp1/inventory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['books'] = Book.objects.all()
        context['inventory_with_borrowed'] = [
            {
                'inventory': inv,
                'borrowed_count': BorrowedBook.get_borrowed_books_count(inv.book)
            }
            for inv in Inventory.objects.all()
        ]
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        user_id = request.POST.get('userid')
        book_id = request.POST.get('bookid')

        if not user_id or not book_id:
            messages.error(request, "User ID and Book ID are required.")
            return redirect('show_inventory')

        if action == 'borrow':
            return self.return_borrow_book(request, user_id, book_id, False)
        elif action == 'return':
            return self.return_borrow_book(request, user_id, book_id, True)
        else:
            messages.error(request, "Invalid action.")
            return redirect('show_inventory')

    def return_borrow_book(self, request, user_id, book_id, choice):

        user = User.objects.get(user_id=user_id)
        book = Book.objects.get(book_id=book_id)

        if choice:
            success, message = BorrowedBook.return_borrowed_book(user, book)
        else:
            success, message = BorrowedBook.add_borrowed_book(user, book)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect('show_inventory')


# ListView for Borrowed Books
class BorrowedBookListView(LoginRequiredMixin, ListView):
    model = BorrowedBook
    template_name = 'demoapp1/borrowed.html'
    context_object_name = 'borrowed_books'


# All the books borrowed by a user logged in


class UserBorrowedBooksView(LoginRequiredMixin, ListView):
    model = BorrowedBook
    template_name = 'demoapp1/user_borrowed_books.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        # Base queryset for the logged-in user
        queryset = BorrowedBook.objects.filter(user=self.request.user)

        # Get filter parameters from the GET request
        author_name = self.request.GET.get('author_name')
        book_name = self.request.GET.get('book_name')

        # Apply filters based on provided parameters
        if author_name:
            queryset = queryset.filter(book__author_name__icontains=author_name)
        if book_name:
            queryset = queryset.filter(book__book_name__icontains=book_name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add context for authors
        context['authors'] = Book.objects.values_list('author_name', flat=True).distinct()
        context['book_names'] = Book.objects.values_list('book_name', flat=True).distinct()
        return context
