from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='1', permanent=True)),
    path('<int:page_id>/', views.home, name='home'),
    path('users/register',views.register_user,name='signup-page'),
    path('users/view',views.view_users,name='list-users'),
    path('users/delete/<int:user_id>',views.delete_user, name ='delete-user'),
    path('users/edit/<int:user_id>',views.edit_user, name ='edit-user'),
    path('journalists/view',views.view_journalists,name='list-journalists'),
    path('journalists/edit/<int:user_id>',views.edit_journalist, name ='edit-journalist'),
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
    path('pages/search/<int:page_id>', views.newssearch, name='combined-search'),
    path('pages/comment', views.newscomment, name='news-comment'),
    path('change_password/', views.change_password, name='change_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)