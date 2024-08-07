from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.generic import (ListView, DeleteView,
                                  UpdateView, CreateView,
                                  TemplateView)
from django.urls import reverse_lazy

from .forms.user_form import UserForm
from .models.book import Book
from .models.inventory import Inventory
from .models.user import User
from .models.borrowed_book import BorrowedBook
from django.contrib.auth.mixins import LoginRequiredMixin


# ListView for Users
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'demoapp1/users.html'
    context_object_name = 'users'


# DeleteView for Users
class UserDeleteView(DeleteView, LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('show_user')
    pk_url_kwarg = 'user_id'


# UpdateView for User
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'demoapp1/edit_form.html'
    context_object_name = 'user'
    success_url = reverse_lazy('show_user')
    pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        # Check if email exists for another user
        if User.objects.filter(email=email):
            form.add_error('email', 'A user with this email already exists.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'User'
        context['edit_url'] = 'edit_user'
        return context


# ListView for Books
class BookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'demoapp1/books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.select_related('inventory')


# CreateView for User
class BookCreateView(CreateView):
    model = Book
    fields = ['book_name', 'author_name']
    template_name = 'demoapp1/books.html'
    context_object_name = 'book'
    success_url = reverse_lazy('show_book')

    def form_valid(self, form):

        book_name = form.cleaned_data.get("book_name")
        author_name = form.cleaned_data.get("author_name")
        quantity = self.request.POST.get('book_quantity')

        status = Book.check_book_existence(book_name, author_name)
        if status:
            return self.form_invalid(form)
        book = form.save()
        Inventory.add_inventory(book, quantity)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Redirect to books list with error message
        messages.error(self.request,
                       "Cant add the already existing book")
        return redirect('show_book')


# UpdateView for Books
class BookUpdateView(UpdateView):
    model = Book
    fields = ['book_name', 'author_name']
    template_name = 'demoapp1/edit_form.html'
    context_object_name = 'book'
    success_url = reverse_lazy('show_book')
    pk_url_kwarg = 'book_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Book'
        context['edit_url'] = 'edit_book'
        return context

    def form_invalid(self, form):
        # it will catch the model uniqueness errors (model cant have
        # entry with same author_name and book_name)
        print(form.errors)
        return super().form_invalid(form)


# DeleteView for Books
class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('show_book')
    pk_url_kwarg = 'book_id'


# ListView for Inventory
class InventoryListView(LoginRequiredMixin, ListView):
    model = Inventory
    template_name = 'demoapp1/inventory.html'
    context_object_name = 'inventory_with_borrowed'

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

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to home page after successful signup
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'demoapp1/auth_form.html', {'form': form,
                                                       'is_signup': True})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'demoapp1/auth_form.html', {'form': form,
                                                       'is_signup': False})


