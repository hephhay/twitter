# Generated by Django 4.1.2 on 2022-10-16 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_reply_created_by_alter_reply_likes_and_more'),
        ('users', '0006_notification_bookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='reply',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_reply', to='users.bookmark'),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='tweet',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_post', to='post.tweet'),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='reply',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_reply', to='users.notification'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='tweet',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_post', to='post.tweet'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
