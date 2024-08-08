from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (ListView, DeleteView,
                                  UpdateView, CreateView)
from django.urls import reverse_lazy
from demoapp1.models.book import Book
from demoapp1.models.inventory import Inventory
from django.contrib.auth.mixins import LoginRequiredMixin


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


# DeleteView for Books
class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('show_book')
    pk_url_kwarg = 'book_id'
