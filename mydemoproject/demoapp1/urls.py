"""
URL configuration for mydemoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views

from demoapp1.views.book import (BookCreateView,
                                 BookListView, BookUpdateView,
                                 BookDeleteView,
                                 )
from demoapp1.views.borrowed import BorrowReturnView, BorrowedBookListView

from demoapp1.views.inventory import InventoryListView
from demoapp1.views.password_reset import (CustomPasswordResetConfirmView,
                                           CustomPasswordResetCompleteView)
from demoapp1.views.signup_signin import signup, signin
from demoapp1.views.user import (UserUpdateView, UserListView,
                                 UserDeleteView, UserAddView)


urlpatterns = [

    # common views
    path('signup/', signup, name='signup'),
    path('', signin, name='signin'),
    path('signin/', signin, name='signin'),
    path('logout/', LogoutView.as_view(next_page='signin'), name='logout'),

    # paths of book
    path('books/', BookListView.as_view(), name='show_book'),
    path('books/<int:book_id>/edit/', BookUpdateView.as_view(), name='edit_book'),
    path('books/<int:book_id>/delete/', BookDeleteView.as_view(), name='delete_book'),
    path('books/add/', BookCreateView.as_view(), name='add_book'),

    # paths of users
    path('users/', UserListView.as_view(), name='show_user'),
    path('users/add/', UserAddView.as_view(), name='add_user'),
    path('users/<int:user_id>/edit/', UserUpdateView.as_view(), name='edit_user'),
    path('users/<int:user_id>/delete/', UserDeleteView.as_view(), name='delete_user'),

    # paths of inventory
    path('inventory/', InventoryListView.as_view(), name='show_inventory'),
    path('inventory/borrow/', BorrowReturnView.as_view(), name='borrow_book'),
    path('inventory/return/', BorrowReturnView.as_view(), name='return_book'),

    # paths for borrowed books
    path('borrowed/', BorrowedBookListView.as_view(), name='show_borrowed'),

    # paths for user-specific views
    path('books/', BookListView.as_view(), name='show_books'),
    path('user/borrowed/', BorrowedBookListView.as_view(), name='show_borrowed_books'),

    # Django's built-in password reset views
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # this view is Overriden parent view = PasswordResetConfirmView
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
