from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def show_books(request):
    return render(request, 'demoapp1/books.html')

def show_users(request):
    return render(request, 'demoapp1/users.html')


def show_inventory(request):
    return render(request, 'demoapp1/inventory.html')

def show_borrowed(request):     
    return render(request, 'demoapp1/borrowed.html')
