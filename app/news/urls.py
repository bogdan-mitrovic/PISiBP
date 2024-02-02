from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health', views.health, name='health'),
    path('users/register',views.register_user,name='signup-page'),
    path('users/view',views.view_users,name='list-users'),
    path('users/delete/<int:user_id>',views.delete_user, name ='delete-user'),
    path('users/edit/<int:user_id>',views.edit_user, name ='edit-user'),
    path('drafts/view',views.view_drafts,name='list-drafts'),
    path('drafts/detail/<int:draft_id>',views.draftdetail, name ='view-draft'),
    path('drafts/delete/<int:draft_id>',views.delete_draft, name ='delete-draft'),
    path('drafts/approve/<int:draft_id>',views.approve_draft, name ='approve-draft'),
    path('draft/edit/<int:draft_id>',views.edit_draft, name ='edit-draft'),
    path('pages/add',views.add,name='add-news-page'),
    path('pages/edit/<int:news_id>',views.edit, name ='edit-news'),
    path('pages/delete/<int:news_id>',views.delete, name ='delete-news'),
    path('pages/news/<int:news_id>', views.newsdetail, name='news-detail'),
    path('pages/like/<int:news_id>', views.newslike, name='like-news'),
    path('pages/dislike/<int:news_id>', views.newsdislike, name='dislike-news'),
    path('pages/comment/like/<int:comment_id>', views.commentlike, name='like-comment'),
    path('pages/comment/dislike/<int:comment_id>', views.commentdislike, name='dislike-comment'),
    path('pages/search', views.newssearch, name='combined-search'),
    path('pages/comment', views.newscomment, name='news-comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)