# Generated by Django 5.0.7 on 2024-07-26 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp1', '0007_remove_borrowedbook_unreturned_books_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='borrow_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='borrowedbook',
            name='return_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('author_name', 'book_name'), name='unique_author_book'),
        ),
    ]
