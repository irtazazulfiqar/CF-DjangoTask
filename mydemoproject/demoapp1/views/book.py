from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import (ListView, DeleteView,
                                  UpdateView, CreateView)
from django.urls import reverse_lazy
from demoapp1.models.book import Book
from demoapp1.models.inventory import Inventory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from demoapp1.views.permissions_user import user_only


class BaseBookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 2

    def get_queryset(self):
        queryset = Book.objects.select_related('inventory').order_by('book_id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(book_name__icontains=query) | Q(author_name__icontains=query)
            )
        return queryset


# ListView for Books
class BookListView(PermissionRequiredMixin, BaseBookListView):
    template_name = 'demoapp1/books.html'
    permission_required = 'demoapp1.view_book_admin'


class UserBookListView(PermissionRequiredMixin, BaseBookListView):
    template_name = 'demoapp1/book_list_user.html'
    permission_required = 'demoapp1.view_book_newuser'

    def dispatch(self, request, *args, **kwargs):
        return user_only(super().dispatch)(request, *args, **kwargs)


# CreateView for User
class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['book_name', 'author_name']
    template_name = 'demoapp1/books.html'
    context_object_name = 'book'
    success_url = reverse_lazy('show_book')
    permission_required = 'demoapp1.add_book'

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
                       "Book Already Exists")
        return redirect('show_book')


# UpdateView for Books
class BookUpdateView(PermissionRequiredMixin,UpdateView):
    model = Book
    fields = ['book_name', 'author_name']
    template_name = 'demoapp1/edit_form.html'
    context_object_name = 'book'
    success_url = reverse_lazy('show_book')
    pk_url_kwarg = 'book_id'
    permission_required = 'demoapp1.change_book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Book'
        context['edit_url'] = 'edit_book'
        return context


# DeleteView for Books
class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('show_book')
    pk_url_kwarg = 'book_id'
    permission_required = 'demoapp1.delete_book'

