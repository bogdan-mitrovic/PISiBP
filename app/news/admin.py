from django.contrib import admin

# Register your models here.
from .models import Category, Comment, News

admin.site.register(Category)
admin.site.register(News)
admin.site.register(Comment)

