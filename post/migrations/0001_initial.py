# Generated by Django 4.1.2 on 2022-10-16 19:11

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(null=True, verbose_name='content')),
                ('media', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, verbose_name='media files'), default=list, size=None)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creator', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(null=True, verbose_name='content')),
                ('media', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, verbose_name='media files'), default=list, size=None)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_creator', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_reply', to='post.reply')),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_post', to='post.tweet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
