from django.db.models.signals import post_save
from django.dispatch import receiver
from demoapp1.models import BorrowedBook
from demoapp1.utils import send_email_with_context


@receiver(post_save, sender=BorrowedBook)
def send_borrowed_book_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        book = instance.book
        due_date = instance.due_date.strftime('%Y-%m-%d')

        # Prepare email content
        subject = f"Borrowed Book: {book.book_name}"
        send_email_with_context(subject, user.email, 'borrowed_book_email.html',
                                {
                                    'username': user.username,
                                    'book_name': book.book_name,
                                    'author_name': book.author_name,
                                    'due_date': due_date,
                                })
