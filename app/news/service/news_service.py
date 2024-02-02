from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import F
from django.db.models import Count
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django import forms
from ..models import Category
from ..models import News
from ..models import News_draft
from ..models import Likes
from ..models import Comment
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
class NewsService():
    def __init__(self):
        pass

    def getAll(self):
        news = None
        try:
            news = News.objects.all()
        except Exception as e: raise Http404("DB Error: Cant get all news")
        return news
    
    def getById(self, id):
        news = None
        try:
            news = News.objects.get(id=id)
        except Exception as e: raise Http404("DB Error: Cant get news by id")
        return news
    
    def getAllByCategoryId(self, id):
        try:
            news = News.objects.filter(category_id=id)
        except Exception as e: raise Http404("DB Error: Cant get news by category id")
        return news

    def search(self, keyword, id, date):
        news=News.objects.all()
        if keyword:
            try:
                news = news.filter(Q(content__icontains=keyword) | Q(title__icontains=keyword) | Q(tags__name__icontains=keyword))
            except Exception as e: raise Http404("DB Error: cant get searched news")

        if id:
            try:
                news = news.filter(category_id=id)
            except Exception as e: raise Http404("DB Error: Cant get news by category id")

        if date:
            try:
                news = news.filter(Q(publish_date__icontains=date))
            except Exception as e: raise Http404("DB Error: Cant get news by date")
        return news

    def updateViewCount(self, news_id):
        try:
            News.objects.filter(id=news_id).update(views=F('views')+1)
        except Exception as e: raise Http404("DB Error: cant update the view count")
    
    def getRecentMostCommentedNews(self):
        try:
            check_date = timezone.now() + relativedelta(months=-settings.RECENT_NEWS_MONTH)
            news = Comment.objects.filter(news__publish_date__gt=check_date).values('news_id', 'news__title', 'news__views').annotate(total=Count('news_id'))
            return news
        except Exception as e: raise Http404("DB Error: cant get the most commented news") 

    def saveNewNews(self, form_data):
        try:
            cat = CategoryService().getByCategoryId(form_data["category_id"])
            date = timezone.now()
            """try:
                image_file = form_data["image"]
                image = Image(img=image_file)
                image.save()
            except Exception as e: raise Http404("Couldn't create/save image") 
            """
            news = News(title=form_data["title"], tags = form_data["tags"], content = form_data["content"], category = cat, publish_date=date)
            news.save()
        except Exception as e: raise Http404("DB Error: Could not save news") 


class CategoryService():
    def __init__(self):
        pass

    def getAll(self):
        try:
            categories = Category.objects.all()
        except Exception as e: raise Http404("DB Error: cant get all categories")
        return categories 
    def getByCategoryId(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Exception as e: raise Http404("DB Error: cant get category by category id")
        return category 
        

class CommentService():
    def __init__(self):
        pass
    
    def getById(self, id):
        comment = None
        try:
            comment = Comment.objects.get(id=id)
        except Exception as e: raise Http404("DB Error: Cant get news by id")
        return comment
    

    def getByNewsId(self, news_id):
        try:
            comments = Comment.objects.filter(news_id=news_id)
        except Exception as e: raise Http404("DB Error: cant get comment by news id")
        return comments 

    def saveNewComment(self, form_data):
        try:
            date = timezone.now()
            news = NewsService().getById(form_data["news_id"])
            comments = Comment(text=form_data["text"], news = news, user = form_data["user"], tmp_username=form_data["tmp_username"], publish_date = date)        
            comments.save()
        except Exception as e: raise Http404("DB Error: Could not save comment")


class Add_news_Form(forms.ModelForm):
    title = forms.CharField(max_length = 50, required=True)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    image = forms.ImageField(required=False)
    is_up_for_review = forms.BooleanField(required=False)
    class Meta:
        model = News_draft
        fields = ['title', 'tags', 'content', 'category', 'image', 'is_up_for_review' ]


class Edit_news_Form(forms.ModelForm):
    title = forms.CharField(max_length = 50, required=True)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    image = forms.ImageField(required=False)
    class Meta:
        model = News
        fields = ['title', 'tags', 'content', 'image']






class UsersService():
    def __init__(self):
        pass

    def getAll(self):
        users = None
        try:
            users = User.objects.all()
        except Exception as e: raise Http404("DB Error: Cant get all users")
        return users
    
    def getById(self, id):
        users = None
        try:
            users = User.objects.get(id=id)
        except Exception as e: raise Http404("DB Error: Cant get user by id")
        return users
    

class DraftsService():
    def __init__(self):
        pass

    def getAll(self):
        drafts = None
        try:
            drafts = News_draft.objects.all()
        except Exception as e: raise Http404("DB Error: Cant get all drafts")
        return drafts
    
    def getById(self, draft_id):
        draft = None
        try:
            draft = News_draft.objects.get(id=draft_id)
        except Exception as e: raise Http404("DB Error: Cant get user by id")
        return draft
    

    def getByNewsId(self, news_id):
        drafts = None
        try:
            drafts = News_draft.objects.get(draft_of_id=news_id)
        except Exception as e: raise Http404("DB Error: Cant get draft by news id")
        return drafts
    

