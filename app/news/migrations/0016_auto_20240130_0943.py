# Generated by Django 3.2.23 on 2024-01-30 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0015_remove_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='news_draft',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='news_draft',
            name='was_seen_by_editor',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
