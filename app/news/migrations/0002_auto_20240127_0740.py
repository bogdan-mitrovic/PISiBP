# Generated by Django 3.2.23 on 2024-01-27 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('is_news', models.BooleanField(null=True)),
                ('like_identifier', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='news',
            name='like_identifier',
        ),
        migrations.RemoveField(
            model_name='news',
            name='likes',
        ),
        migrations.AddField(
            model_name='news',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
