from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.models import Count, F, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from tinymce.widgets import TinyMCE

from .models import Category, Comment, News, News_draft

news_per_page=15


#used for queries on News
class NewsService():
    def __init__(self):
        pass

    def getbyPageId(self,page_id):
        news = None
        try:
            news = News.objects.all()
        except Exception as e: raise Http404("DB Error: Cant get all news")
        if news and news.count()>=news_per_page:
            last_page = news.count() / news_per_page
            page_id = last_page if page_id > last_page else page_id
            news = news[news_per_page*(page_id-1):news_per_page*page_id]
            return news, last_page
        else:
            return news,1
    
    def getById(self, id):
        news = None
        try:
            news = News.objects.get(id=id)
        except Exception as e: raise Http404("DB Error: Cant get news by id")
        return news
    
    def search(self, keyword, id, date1, date2, page_id):
        news=News.objects.all()
        if keyword:
            try:
                news = news.filter(Q(title__icontains=keyword) | Q(tags__name__icontains=keyword))
            except Exception as e: raise Http404("DB Error: cant get searched news")

        if id:
            try:
                news = news.filter(category_id=id)
            except Exception as e: raise Http404("DB Error: Cant get news by category id")



        start_date=  timezone.make_aware(datetime.strptime(date1, '%Y-%m-%d')) if date1 else timezone.make_aware(datetime.strptime('1970-1-1', '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(date2, '%Y-%m-%d')) if date2 else timezone.make_aware(datetime.now())
        if start_date != end_date:
            try:
                 news = news.filter(publish_date__range=[start_date, end_date])
            except Exception as e: raise Http404("DB Error: Cant get news by date")
        elif start_date == end_date:
            try:
                news = news.filter(Q(publish_date__icontains=date1))
            except Exception as e: raise Http404("DB Error: Cant get news by date")
        news = news.distinct()
        if news and news.count()>=news_per_page:
            
            last_page = news.count() / news_per_page
            page_id = last_page if page_id > last_page else page_id
            news = news[news_per_page*(page_id-1):news_per_page*page_id]
            return news, last_page
        else:
            return news,1

    def updateViewCount(self, news_id):
        try:
            News.objects.filter(id=news_id).update(views=F('views')+1)
        except Exception as e: raise Http404("DB Error: cant update the view count")
    
#used for queries on Category
class CategoryService():
    def __init__(self):
        pass

    def getAll(self):
        try:
            categories = Category.objects.all()
        except Exception as e: raise Http404("DB Error: cant get all categories")
        return categories 

#used for queries on Comment
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
            comments = Comment(text=form_data["text"], news = news, tmp_username=form_data["tmp_username"], publish_date = date)        
            comments.save()
        except Exception as e: raise Http404("DB Error: Could not save comment")



#used for queries on Users
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
    
    def getJournalists(self):
        users = None
        try:
            users = User.objects.all()
            users = users.filter(is_superuser = False, is_staff = False)
        except Exception as e: raise Http404("DB Error: Cant get all users")
        return users
    
#used for queries on News_draft
class DraftsService():
    def __init__(self):
        pass
    
    def getById(self, draft_id):
        draft = None
        try:
            draft = News_draft.objects.get(id=draft_id)
        except Exception as e: raise Http404("DB Error: Cant get draft by user id")
        return draft
    

    def getByNewsId(self, news_id):
        drafts = None
        try:
            drafts = News_draft.objects.filter(draft_of_id=news_id)
        except Exception as e: raise Http404("DB Error: Cant get draft by news id")
        return drafts
    
    def getByCreatorId(self, user_id):
        drafts = None
        try:
            drafts = News_draft.objects.filter(creator_id=user_id)
        except Exception as e: raise Http404("DB Error: Cant get draft by creator id")
        return drafts
    
    def getAll_Up_for_review(self):
        drafts = None
        try:
            drafts = News_draft.objects.all()
            drafts= drafts.filter(is_up_for_review = True)
        except Exception as e: raise Http404("DB Error: Cant get all drafts")
        return drafts
    
    def getAllByCategory_Up_for_review(self, categories):
        try:
            drafts = News_draft.objects.filter(category_id__in=categories)
            drafts= drafts.filter(is_up_for_review = True)
        except Exception as e: raise Http404("DB Error: Cant get news by category id")
        return drafts
    



def get_like_identifier(request):
    # Use a cookie to identify authenticated users
    if request.user.is_authenticated:
        return str(request.user.id)
    else:
        # For anonymous users, use a combination of IP address and a constant string
        ip_address = get_client_ip(request)
        constant_part = "anonymous_like_identifier"
        like_identifier = f"{ip_address}-{constant_part}"

        response = HttpResponse()
        response.set_cookie('like_identifier', like_identifier)
        return like_identifier

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



#way of putting news in "Trending"
def getTrendingNews():
    return News.objects.order_by('-views','-likes','-dislikes')[:5]
