from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.core import serializers
from django import forms

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .service.authentication import CustomUserCreationForm
from .service.news_service import CategoryService
from .service.news_service import NewsService
from .service.news_service import CommentService
from .service.news_service import LikesService
from .service.news_service import UsersService
from .service.news_service import Add_news_Form
from .models import News
from .models import Like
user_not_supported =  {"error":"User not supported"}
method_not_supported = {"error":"method not supported"}
invalid_form = {"error":"invalid form"}

#### Controllers
def health(request):
    return HttpResponse("Application news portal Started", content_type="text/plain")

def home(request):
    if request.user.is_authenticated:
        categories = CategoryService().getAll()
        news = NewsService().getAll()
        context = {
            "categories":categories,
            "news":getPreviewNews(news),
            "trend":getTrendingNews()
        }
        return render(request, 'dashboard.html', context)
    else:
        categories = CategoryService().getAll()
        news = NewsService().getAll()
        
        context = {
            "categories":categories,
            "news":getPreviewNews(news),
            "trend":getTrendingNews()
        }
        return render(request, 'home.html', context)
    

def view_users(request):
    users = UsersService().getAll()
    context = {
            "users":users,
    }
    return render(request, 'users.html', context)





def add(request):
    if request.method == 'POST':
        form = Add_news_Form(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            # Access form data using form.cleaned_data dictionary
            form_data = dict(form.cleaned_data)
            if "category_id" in request.POST:
                form_data["category_id"]=request.POST["category_id"] 
            # Add your logic here
            NewsService().saveNewNews(form_data)
            return redirect('home')
        else:
                return JsonResponse(invalid_form, safe=False) 
    else:
        form = Add_news_Form()
    categories = CategoryService().getAll()
    context = {
        "categories":categories,
        "form":form
    }
    return render(request, 'add_news.html', context)



def delete(request, news_id):
    news = NewsService().getById(news_id)
    try:
        news.delete()
    except Exception as e: raise Http404("DB Error: Cant delete news")
    return redirect('home')

def delete_user(request, user_id):
    user = UsersService().getById(user_id)
    try:
        user.delete()
    except Exception as e: raise Http404("DB Error: Cant delete user")
    return redirect('list-users')



def edit_user(request, user_id):
    user = UsersService().getById(user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,instance=user)
        form.fields['password1'].required = False
        form.fields['password2'].required = False
        if form.is_valid():
            form.save()
            # Redirect or do other actions upon successful registration
            return redirect('list-users')
        else:
            return JsonResponse(invalid_form, safe=False) 
    else:
        form = CustomUserCreationForm(instance=user)
        form.fields['password1'].required = False
        form.fields['password2'].required = False
    context = {
            "user":user,
            "form":form,
    }
        #return JsonResponse(list(comments), safe=False)
    return render(request, 'edit_user.html', context)

def register_user(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            # Redirect or do other actions upon successful registration
            return redirect('home')
        else:
            return JsonResponse(invalid_form, safe=False) 
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})



def edit(request, news_id):
    if request.method == 'POST':
        form = Add_news_Form(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            # Access form data using form.cleaned_data dictionary
            form_data = dict(form.cleaned_data)
            if "category_id" in request.POST:
                form_data["category_id"]=request.POST["category_id"] 
            # Add your logic here
            NewsService().saveNewNews(form_data)
            return redirect('home')
        else:
            return JsonResponse(invalid_form, safe=False) 
    else:
        news = NewsService().getById(news_id)
        form = Add_news_Form(initial={'title':news.title,
                                    'content':news.content,
                                    'tags':news.tags,
                                    'image':news.image,})
        
    context = {
            "news":news,
            "categories": getCategory(request),
            "form":form,
    }
        #return JsonResponse(list(comments), safe=False)
    return render(request, 'edit_news.html', context)




def newsdetail(request, news_id):
    news = NewsService().getById(news_id)
    comments = CommentService().getByNewsId(news_id)
    form = MessageForm(initial={'news_id':news_id})
    
    NewsService().updateViewCount(news_id)
    news.views = news.views +1
    context = {
        "news":news,
        "categories": getCategory(request),
        "comments": comments,
        "form":form,
        "trend":getTrendingNews()
    }
    #return JsonResponse(list(comments), safe=False)
    return render(request, 'content.html', context)


def newscomment(request):
    if(request.method=="POST"):
        form = MessageForm(request.POST)
        if form.is_valid():
            #print("break point 1")
            form_data = dict(form.cleaned_data)
            if request.user.is_authenticated:
                form_data["user"] = request.user
                form_data["tmp_username"] = None
            if not request.user.is_authenticated and "tmp_username" in request.POST:
                form_data["user"] = None 
                form_data["tmp_username"] = request.POST["tmp_username"] 
            CommentService().saveNewComment(form_data)
            return redirect('news-detail', news_id = form_data["news_id"])
        else:
                return JsonResponse(invalid_form, safe=False) 
    else:
        return JsonResponse(method_not_supported, safe=False)

def newssearch(request):
    search_key = request.GET.get('search')
    category_id = request.GET.get('cat')
    date = request.GET.get('date')
    news = NewsService().search(search_key, category_id, date)

    #print(news)
    categories = getCategory(request)
    context = {
        "categories":categories,
        "news":getPreviewNews(news),
        "trend":getTrendingNews()
    }
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'home.html', context)

## helper methods
def getPreviewNews(news):
    for item in news:
        item.content = item.content[0:250]
    return news

def getTrendingNews():
    mostCommentedNews = NewsService().getRecentMostCommentedNews()
    #print(mostCommentedNews)
    trending = []
    for news in mostCommentedNews:
        item = {}
        item["id"] = news["news_id"]
        item["title"] = news["news__title"]
        score = news["news__views"] * 1 + news["total"] * 5
        item["score"] = score
        trending.append(item)

    trending = sorted(trending, key=lambda k: k['score'], reverse=True) 

    return trending[:5]

def getCategory(request):
    return CategoryService().getAll()

class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea ,  label='Comment', max_length=100)
    news_id = forms.CharField()
    text.widget.attrs.update({'class':'form-control', 'rows':'5'})
    news_id.widget = forms.HiddenInput()

    

def newslike(request, news_id):
    news = NewsService().getById(news_id)
    likes = LikesService().getNews()
    # Get the unique identifier for the like
    like_identifier = get_like_identifier(request)


    if likes.filter(like_identifier=like_identifier).exists():
        like=likes.get(like_identifier=like_identifier)
        if not like.is_dislike:
            like.delete()
            news.likes-=1
            news.save()
        else:
            news.likes+=1
            news.dislikes-=1
            news.save()
            like.is_dislike = False
            like.save()
    else:
        news.likes+=1
        news.save()
        like = Like(like_identifier=like_identifier, is_news=True, object_id=news.id, is_dislike=False)
        try:
            like.save()
        except Exception as e: raise Http404("DB Error: Cant save like")

    return redirect('news-detail', news_id = news_id)


def newsdislike(request, news_id):
    news = NewsService().getById(news_id)
    likes = LikesService().getNews()
    # Get the unique identifier for the like
    like_identifier = get_like_identifier(request)


    if likes.filter(like_identifier=like_identifier).exists():
        like=likes.get(like_identifier=like_identifier)
        if like.is_dislike:
            like.delete()
            news.dislikes-=1
            news.save()
        else:
            news.dislikes+=1
            news.likes-=1
            news.save()
            like.is_dislike = True
            like.save()
    else:
        news.dislikes+=1
        news.save()
        like = Like(like_identifier=like_identifier, is_news=True, object_id=news.id, is_dislike=True)
        try:
            like.save()
        except Exception as e: raise Http404("DB Error: Cant save like")

    return redirect('news-detail', news_id = news_id)




def commentlike(request, comment_id):
    comment = CommentService().getById(comment_id)
    likes = LikesService().getComments()
    # Get the unique identifier for the like
    like_identifier = get_like_identifier(request)


    if likes.filter(like_identifier=like_identifier).exists():
        like=likes.get(like_identifier=like_identifier)
        if not like.is_dislike:
            like.delete()
            comment.likes-=1
            comment.save()
        else:
            comment.likes+=1
            comment.dislikes-=1
            comment.save()
            like.is_dislike = False
            like.save()
    else:
        comment.likes+=1
        comment.save()
        like = Like(like_identifier=like_identifier, is_news=False, object_id=comment.id, is_dislike=False)
        try:
            like.save()
        except Exception as e: raise Http404("DB Error: Cant save like")

    return redirect('news-detail', news_id = comment.news_id)


def commentdislike(request, comment_id):
    comment = CommentService().getById(comment_id)
    likes = LikesService().getComments()
    # Get the unique identifier for the like
    like_identifier = get_like_identifier(request)


    if likes.filter(like_identifier=like_identifier).exists():
        like=likes.get(like_identifier=like_identifier)
        if like.is_dislike:
            like.delete()
            comment.dislikes-=1
            comment.save()
        else:
            comment.dislikes+=1
            comment.likes-=1
            comment.save()
            like.is_dislike = True
            like.save()
    else:
        comment.dislikes+=1
        comment.save()
        like = Like(like_identifier=like_identifier, is_news=False, object_id=comment.id, is_dislike=True)
        try:
            like.save()
        except Exception as e: raise Http404("DB Error: Cant save like")
    return redirect('news-detail', news_id = comment.news_id)


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