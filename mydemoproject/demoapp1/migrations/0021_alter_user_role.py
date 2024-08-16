# Generated by Django 5.0.7 on 2024-08-08 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp1', '0020_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('newuser', 'New User'), ('olduser', 'Old User'), ('admin', 'Admin')], default='newuser', max_length=10),
        ),
    ]
