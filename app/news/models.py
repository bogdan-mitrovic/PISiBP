import os
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# Create your models here.



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    alt_text = models.CharField(null=True, max_length = 50)
    url = models.CharField(null=True, blank=True, max_length = 200)
    img = models.ImageField(upload_to="image", blank=True)

    def __str__(self):
        return self.alt_text

class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(null=True, max_length = 50)
    content = HTMLField(max_length = 5000)
    publish_date = models.DateTimeField('date published')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.CharField(null=True, max_length = 50)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    object_id = models.PositiveIntegerField()
    is_news = models.BooleanField(null=True)
    is_dislike = models.BooleanField(null=True, default= False)
    like_identifier = models.CharField(max_length=255, blank=True, null=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    news = models.ForeignKey(News, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tmp_username = models.CharField(null=True, max_length = 50)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.text





