# Generated by Django 5.0.7 on 2024-07-26 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp1', '0006_alter_borrowedbook_user'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='borrowedbook',
            name='unreturned_books',
        ),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together=set(),
        ),
    ]
