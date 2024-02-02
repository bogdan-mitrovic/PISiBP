# Generated by Django 3.2.23 on 2024-01-27 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20240127_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='is_dislike',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
    ]