# Generated by Django 4.1.2 on 2022-10-16 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=100, null=True, verbose_name='location'),
        ),
    ]
