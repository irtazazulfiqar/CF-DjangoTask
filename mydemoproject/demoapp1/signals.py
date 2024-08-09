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

        # HTML content for the email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Borrowed Book Confirmation</title>
        </head>
        <body>
            <p>Dear {user.username},</p>
            <p>Thank you for borrowing "<strong>{book.book_name}</strong>" by {book.author_name}.</p>
            <p>You need to return it by <strong>{due_date.strftime('%Y-%m-%d')}</strong>.</p>
            <p>Best regards,<br>
            Library Team</p>
            <p><img src="https://feji.us/ngrv2f" alt="Library Logo" style="width: 150px; height: auto;"></p>
        </body>
        </html>
        """

        # Send email using SendGrid
        sendgrid_client = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        subject = f"Borrowed Book: {book.book_name}"

        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )

        # Disable SSL verification if needed
        ssl._create_default_https_context = ssl._create_unverified_context

        # Send the email
        response = sendgrid_client.send(mail)

