from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import BorrowedBook
import sendgrid
from sendgrid.helpers.mail import Mail
import ssl


@receiver(post_save, sender=BorrowedBook)
def send_borrowed_book_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        book = instance.book
        due_date = instance.due_date

        email_content = f"""
        Dear {user.username},

        Thank you for borrowing "{book.book_name}" by {book.author_name}.

        You need to return it by {due_date.strftime('%Y-%m-%d')}.

        Best regards,
        Library Team
        """

        # Send email using SendGrid
        sendgridcall = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        subject = f"Borrowed Book: {book.book_name}"

        mail = Mail(from_email, to_email, subject, email_content)

        """
            We need to disable SSL verification otherwise it will perform 
            SSL verification
        """

        ssl._create_default_https_context = ssl._create_unverified_context

        response = sendgridcall.send(mail)

