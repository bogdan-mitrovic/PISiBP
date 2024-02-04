from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.core import serializers
from django import forms
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from .service.authentication import CustomUserCreationForm
from .service.authentication import CustomUserEditForm
from .service.authentication import CustomJournalistEditForm
from .service.news_service import CategoryService
from .service.news_service import NewsService
from .service.news_service import CommentService
from .service.news_service import UsersService
from .service.news_service import DraftsService
from .service.news_service import Add_news_Form
from .service.news_service import Edit_news_Form
from .service.news_service import Edit_draft_Form
from .models import News
from .models import News_draft
from .models import Likes
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
user_not_supported =  {"error":"User not supported"}
method_not_supported = {"error":"method not supported"}
invalid_form = {"error":"invalid form"}
import os
#### Controllers
def health(request):
    return HttpResponse("Application news portal Started", content_type="text/plain")

def home(request):
        categories = CategoryService().getAll()
        news = NewsService().getAll()
        context = {
            "categories":categories,
            "trend":getTrendingNews(),
            "news":news,
        }
        return render(request, 'home.html', context)
    

def view_users(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = UsersService().getAll()
        categories = CategoryService().getAll()
        context = {
                "categories":categories,
                "users":users,
        }
        return render(request, 'users.html', context)
    else:
        return redirect('home')
    


def view_journalists(request):
    if request.user.is_authenticated and request.user.is_staff and not request.user.is_superuser:
        users = UsersService().getAll()
        users = users.filter(is_superuser = False, is_staff = False)
        categories = CategoryService().getAll()
        context = {
                "categories":categories,
                "users":users,
        }
        return render(request, 'journalists.html', context)
    else:
        return redirect('home')
    


def edit_journalist(request, user_id):
    if request.user.is_authenticated and request.user.is_staff and not request.user.is_superuser:
        user = UsersService().getById(user_id)
        editor_categories = request.user.user_profile.categories.all()

        if request.method == 'POST':
            form = CustomJournalistEditForm(request.POST, instance=user,editor_categories = editor_categories )

            if form.is_valid():
                form.save()
                user.user_profile.categories.set(form.clean_categories())
                # Redirect or do other actions upon successful user edit
                return redirect('list-journalists')
            else:
                form_errors = dict([(field, [error for error in errors]) for field, errors in form.errors.items()])
                context = {"user": user,'form': form, 'form_errors': form_errors}
                return render(request, 'edit_journalist.html', context)
    
        else:
            form = CustomJournalistEditForm(instance=user, editor_categories = editor_categories)

        context = {
            "user": user,
            "form": form,
        }

        return render(request, 'edit_journalists.html', context)
    else:
        return redirect('home')
    


def view_drafts(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            drafts = DraftsService().getAll()
            drafts= drafts.filter(is_up_for_review = True)
        else:
            if not request.user.is_staff:
                drafts = DraftsService().getByCreatorId(request.user.id)
            else:
                drafts = DraftsService().getAllByCategory(request.user.user_profile.categories.all())
                drafts= drafts.filter(is_up_for_review = True)
        categories = CategoryService().getAll()
        context = {
                "categories":categories,
                "drafts":drafts,
        }
        return render(request, 'drafts.html', context)
    else:
        return redirect('home')




def add(request):
    if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
        categories = request.user.user_profile.categories.all()
        if request.method == 'POST':
            form = Add_news_Form(request.POST, request.FILES, category_queryset=categories)
            if form.is_valid():
                # Process the form data
                # Access form data using form.cleaned_data dictionary
                news=form.save(commit=False)

                # Add your logic here
                date = timezone.now()
                news.publish_date = date
                news.creator = request.user
                news.save()
                news.tags.set(form.cleaned_data['tags'])
                return redirect('home')
            else:
                form_errors = dict([(field, [error for error in errors]) for field, errors in form.errors.items()])
                context = {'form': form, 'form_errors': form_errors}
                return render(request, 'add_news.html', context)
        else:
            form = Add_news_Form(category_queryset=categories)
        
        context = {
            "form":form
        }
        return render(request, 'add_news.html', context)
    else:
        return redirect('home')


def delete(request, news_id):
    news = NewsService().getById(news_id)
    if request.user.is_superuser or request.user.is_staff:
        try:
            news.delete()
        except Exception as e: raise Http404("DB Error: Cant delete news")
    else:    
        if request.user.is_authenticated and not (News_draft.objects.filter(draft_of = news, is_up_for_deletion = True)):
            
            draft = News_draft(draft_of = news, is_up_for_deletion = True, title=news.title, is_up_for_review = True, creator = request.user)
            
            try:
                draft.save()
            except Exception as e: raise Http404("DB Error: Cant create draft")
    return redirect('home')




def delete_user(request, user_id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = UsersService().getById(user_id)
        try:
            user.delete()
        except Exception as e: raise Http404("DB Error: Cant delete user")
        return redirect('list-users')
    else:
        return redirect('home')
    


def delete_draft(request, draft_id):
    draft = DraftsService().getById(draft_id)
    if request.user.is_authenticated and (request.user.is_superuser or draft.creator==request.user or (request.user.is_staff and draft.is_up_for_review and (draft.category in request.user.user_profile.categories.all()))):

        try:
            draft.delete()
        except Exception as e: raise Http404("DB Error: Cant delete draft")
        return redirect('list-drafts')
    else:
        return redirect('home')

def edit_user(request, user_id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = UsersService().getById(user_id)

        if request.method == 'POST':
            form = CustomUserEditForm(request.POST, instance=user)

            if form.is_valid():
                form.save()
                user.user_profile.categories.set(form.clean_categories())
                # Redirect or do other actions upon successful user edit
                return redirect('list-users')
            else:
                form_errors = dict([(field, [error for error in errors]) for field, errors in form.errors.items()])
                context = {"user": user,'form': form, 'form_errors': form_errors}
                return render(request, 'edit_user.html', context)
        else:
            form = CustomUserEditForm(instance=user)

        context = {
            "user": user,
            "form": form,
        }

        return render(request, 'edit_user.html', context)
    else:
        return redirect('home')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                # Ensure the user stays logged in by updating the session hash
                update_session_auth_hash(request, user)
                return redirect('home')  # Replace 'profile' with the desired success redirect
            else:
                form_errors = dict([(field, [error for error in errors]) for field, errors in form.errors.items()])
                context = {'form': form, 'form_errors': form_errors}
                return render(request, 'change_password.html', context)
        else:
            form = PasswordChangeForm(request.user)
        
        return render(request, 'change_password.html', {'form': form})
    else:
        return redirect('home')




def register_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                # Redirect or do other actions upon successful registration
                return redirect('home')
            else:
                form_errors = dict([(field, [error for error in errors]) for field, errors in form.errors.items()])
                context = {'form': form, 'form_errors': form_errors}
                return render(request, 'signup.html', context)
        else:
            form = CustomUserCreationForm()

        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('home')



def edit(request, news_id):
    news = NewsService().getById(news_id)
    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff and news.creator==request.user :
        if request.method == 'POST':
                form = Edit_news_Form(request.POST, request.FILES, instance=news)
                if form.is_valid():
                    # Process the form data
                    # Access form data using form.cleaned_data dictionary
                    news_tmp = form.save(commit=False)
                    draft = News_draft(title=news_tmp.title, content=news_tmp.content, image=news_tmp.image, draft_of = news, is_up_for_review = True , creator = request.user, category=news.category)
                    draft.save()
                    draft.tags.set(form.cleaned_data['tags'])
                    return redirect('home')
                else:
                        form_errors = dict([(field, [error for error in errors]) for field, errors in form.errors.items()])
                        context = {'form': form, 'form_errors': form_errors}
                        return render(request, 'edit_news.html', context)
        else:
            form = Edit_news_Form(instance=news)
            
            context = {
                "form":form
            }
            return render(request, 'edit_news.html', context)
    else:
        return redirect('home')







def edit_draft(request, draft_id):
    draft = DraftsService().getById(draft_id)
    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff and draft.creator==request.user :
        
        if request.method == 'POST':
                form = Edit_draft_Form(request.POST, request.FILES, instance=draft)
                if form.is_valid():
                    # Check if the image in the form is different from the existing image
                # Check if the image in the form is different from the existing image


                    form.save()
                    draft.tags.set(form.cleaned_data['tags'])
                    draft.was_seen_by_editor = False
                    draft.save()
                    return redirect('home')
                else:
                        form_errors = dict([(field, [error for error in errors]) for field, errors in form.errors.items()])
                        context = {'form': form, 'form_errors': form_errors}
                        return render(request, 'edit_draft.html', context)
        else:
            form = Edit_draft_Form(instance=draft)
            
            context = {
                "form":form
            }
            return render(request, 'edit_draft.html', context)
    else:
        return redirect('home')







def draftdetail(request, draft_id):
    draft = DraftsService().getById(draft_id)
    if request.user.is_authenticated and (request.user.is_superuser or draft.creator==request.user or (request.user.is_staff and draft.is_up_for_review and (draft.category in request.user.user_profile.categories.all()))):
        if request.user.is_superuser or request.user.is_staff:
            draft.was_seen_by_editor = True
            draft.save()
        categories = CategoryService().getAll()
        context = {
            "categories":categories,
            "draft":draft,
        }
        #return JsonResponse(list(comments), safe=False)
        return render(request, 'draft_content.html', context)
    else:
        return redirect('home')





def approve_draft(request, draft_id):
    draft = DraftsService().getById(draft_id)
    if request.user.is_authenticated and (request.user.is_superuser  or (request.user.is_staff and draft.is_up_for_review and (draft.category in request.user.user_profile.categories.all()))):
        if not draft.draft_of:
            date = timezone.now()
            news = News(title=draft.title, content=draft.content, category=draft.category, publish_date = date, creator = draft.creator)
            draft_tags = draft.tags.all()
            if draft.image:
                # Use the same filename for the news image
                filename = os.path.basename(draft.image.name)
                news.image.save(filename, ContentFile(draft.image.read()), save=False)

            try:
                news.save()
            except Exception as e: raise Http404("DB Error: Cant save news")
            news.tags.set(draft_tags)
            
            try:
                draft.delete()
            except Exception as e: raise Http404("DB Error: Cant delete draft")
        else:
            if not draft.is_up_for_deletion:
                date = timezone.now()
                news = NewsService().getById(draft.draft_of.id)
                if news.image != draft.image:
                    news.image.delete()
                news.title=draft.title
                news.content=draft.content
                if draft.image:
                # Use the same filename for the news image
                    filename = os.path.basename(draft.image.name)
                    news.image.save(filename, ContentFile(draft.image.read()), save=False)

                draft_tags = draft.tags.all()
                try:
                    news.save()
                except Exception as e: raise Http404("DB Error: Cant save news")
                news.tags.set(draft_tags)
                drafts = DraftsService().getByNewsId(draft.draft_of.id)
                try:
                    drafts.delete()
                except Exception as e: raise Http404("DB Error: Cant delete draft(s)")
            else:
                news = NewsService().getById(draft.draft_of.id)
                try:
                    news.delete()
                    
                except Exception as e: raise Http404("DB Error: Cant delete news")
        
    return redirect('home')







def newsdetail(request, news_id):
    news = NewsService().getById(news_id)
    comments = CommentService().getByNewsId(news_id)
    form = MessageForm(initial={'news_id':news_id})
    users_edit = news.creator
    users_delete = UsersService().getAll().filter(
        Q(is_superuser=True) |
        Q(Q(user_profile__categories=news.category) & Q(is_staff=True)) |
        Q(id=news.creator.id)
    )

    NewsService().updateViewCount(news_id)
    news.views = news.views +1
    categories = CategoryService().getAll()
    context = {
        "categories":categories,
        "news":news,
        "users_edit": users_edit,
        "users_delete" : users_delete,
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
            if not request.user.is_authenticated and "tmp_username" in request.POST:
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
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    news = NewsService().search(search_key, category_id, date1, date2)

    #print(news)
    categories = getCategory(request)
    context = {
        "categories":categories,
        "news":news,
        "trend":getTrendingNews()
    }

    return render(request, 'home.html', context)



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
    # Get the unique identifier for the like
    like_identifier = get_like_identifier(request)

    content_type = ContentType.objects.get_for_model(news)

    if Likes.objects.filter(content_type=content_type, object_id=news.id, like_identifier=like_identifier).exists():
        like = Likes.objects.get(content_type=content_type, object_id=news.id, like_identifier=like_identifier)
        if not like.is_dislike:
            like.delete()
            news.likes -= 1
            news.save()
        else:
            news.likes += 1
            news.dislikes -= 1
            news.save()
            like.is_dislike = False
            like.save()
    else:
        news.likes += 1
        news.save()
        like = Likes(like_identifier=like_identifier, content_type=content_type, object_id=news.id, is_dislike=False)
        try:
            like.save()
        except Exception as e:
            raise Http404("DB Error: Cant save like")

    return redirect('news-detail', news_id=news_id)


def newsdislike(request, news_id):
    news = NewsService().getById(news_id)
    # Get the unique identifier for the like
    like_identifier = get_like_identifier(request)
    content_type = ContentType.objects.get_for_model(news)

    if Likes.objects.filter(content_type=content_type, object_id=news.id, like_identifier=like_identifier).exists():
        like = Likes.objects.get(content_type=content_type, object_id=news.id, like_identifier=like_identifier)
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
        like = Likes(like_identifier=like_identifier, content_type=content_type, object_id=news.id, is_dislike=True)
        try:
            like.save()
        except Exception as e: raise Http404("DB Error: Cant save like")

    return redirect('news-detail', news_id = news_id)




def commentlike(request, comment_id):
    comment = CommentService().getById(comment_id)
    # Get the unique identifier for the like
    like_identifier = get_like_identifier(request)

    content_type = ContentType.objects.get_for_model(comment)

    if Likes.objects.filter(content_type=content_type, object_id=comment.id, like_identifier=like_identifier).exists():
        like = Likes.objects.get(content_type=content_type, object_id=comment.id, like_identifier=like_identifier)
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
        like = Likes(like_identifier=like_identifier, content_type=content_type, object_id=comment.id, is_dislike=False)
        try:
            like.save()
        except Exception as e: raise Http404("DB Error: Cant save like")

    return redirect('news-detail', news_id = comment.news_id)


def commentdislike(request, comment_id):
    comment = CommentService().getById(comment_id)
    # Get the unique identifier for the like
    like_identifier = get_like_identifier(request)
    content_type = ContentType.objects.get_for_model(comment)

    if Likes.objects.filter(content_type=content_type, object_id=comment.id, like_identifier=like_identifier).exists():
        like = Likes.objects.get(content_type=content_type, object_id=comment.id, like_identifier=like_identifier)
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
        like = Likes(like_identifier=like_identifier, content_type=content_type, object_id=comment.id, is_dislike=True)
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