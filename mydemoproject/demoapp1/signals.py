from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import BorrowedBook
from .utils import send_email


@receiver(post_save, sender=BorrowedBook)
def send_borrowed_book_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        book = instance.book
        due_date = instance.due_date.strftime('%Y-%m-%d')

        # Prepare email content
        subject = f"Borrowed Book: {book.book_name}"
        html_content = render_to_string('borrowed_book_email.html', {
            'username': user.username,
            'book_name': book.book_name,
            'author_name': book.author_name,
            'due_date': due_date,
        })
        send_email(subject, user.email, html_content=html_content)
