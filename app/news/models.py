import os
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(null=True, max_length = 50)
    content = HTMLField(max_length = 5000)
    publish_date = models.DateTimeField('date published')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    tags = TaggableManager()
    dislikes = models.IntegerField(default=0)
    like = GenericRelation('Likes')
    def __str__(self):
        return self.title
    


class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_dislike = models.BooleanField(default=False)
    like_identifier = models.CharField(max_length=255, blank=True, null=True)
    

class News_draft(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(null=True, max_length = 50)
    content = HTMLField(max_length = 5000)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    tags = TaggableManager()
    draft_of = models.ForeignKey(News, null=True, on_delete=models.CASCADE)
    is_up_for_review = models.BooleanField(null=True)
    is_approved = models.BooleanField(null=True, default = False)
    is_up_for_deletion = models.BooleanField(null=True, default = False)
    def __str__(self):
        return self.title
    

"""

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    object_id = models.PositiveIntegerField()
    is_news = models.BooleanField(null=True)
    is_dislike = models.BooleanField(null=True, default= False)
    like_identifier = models.CharField(max_length=255, blank=True, null=True)
"""



class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    news = models.ForeignKey(News, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tmp_username = models.CharField(null=True, max_length = 50)
    publish_date = models.DateTimeField('date published',null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    like = GenericRelation('Likes')

    def __str__(self):
        return self.text





