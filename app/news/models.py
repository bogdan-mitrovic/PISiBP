import os

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name



#basically extends django's predefined User model
#enabling each user to have privileges for multiple categories
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    categories = models.ManyToManyField(Category, related_name='users_with_privileges')

    def __str__(self):
        return self.user.username





class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(null=True, max_length = 250, db_index=True)
    content = HTMLField(max_length = 5000)
    publish_date = models.DateTimeField('date published')
    views = models.IntegerField(default=0)
    #number of times someone has read it
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    like = GenericRelation('Likes')
    #each news object stores a simple counter
    #while a Likes object keeps track of which objects are liked, and by whom

    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True, blank=True, max_length = 5000)
    tags = TaggableManager()
    
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    #used to determine who can suggest an edit or deletion
    def __str__(self):
        return self.title
    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
    


class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    #used to enable both objects of type News and Comment to be liked / disliked

    is_dislike = models.BooleanField(default=False)
    #a flag to determine if the object is currently a like or a dislike
    like_identifier = models.CharField(max_length=255, blank=True, null=True)
    #a way to disable one user to like/dislike an object multiple times



class News_draft(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(null=True, max_length = 50)
    content = HTMLField(max_length = 5000)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True, blank=True, max_length = 5000)
    tags = TaggableManager()
    draft_of = models.ForeignKey(News, null=True, on_delete=models.CASCADE)
    #keep track of the original news article, if this is an edit
    is_up_for_review = models.BooleanField(null=True)
    #will be used to determine if only the journalists can see it
    #or will it also show up at editor's point of view
    is_up_for_deletion = models.BooleanField(null=True, default = False)
    #this will tell the editor that the journalist has requested the deletion of an article
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    #used to determine who can suggest an edit of a draft, and later on, who is the 
    #creator of a news article
    was_seen_by_editor = models.BooleanField(null=True, default = False)
    #this let's a journalist now that an editor has senn the draft
    #but has neither approved it, nor deleted it
    #so that the journalist can make further changes

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    news = models.ForeignKey(News, null=True, on_delete=models.CASCADE)
    #keep track of the news article that this comment is made for
    tmp_username = models.CharField(null=True, max_length = 50)
    #since commenting doesn't require logging in, this is used 
    publish_date = models.DateTimeField('date published',null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    like = GenericRelation('Likes')
    #same thing as for the news objects
    def __str__(self):
        return self.text





@receiver(pre_delete, sender=News)
@receiver(pre_delete, sender=News_draft)
def delete_news_image(sender, instance, **kwargs):
    # Delete the associated image file when a News or NewsDraft object is deleted
    if instance.image:
        instance.image.delete(save=False)
