# Generated by Django 4.1.2 on 2023-02-10 08:15

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_delete_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to=users.models.user_avatar_path, verbose_name='profile pictire'),
        ),
    ]
