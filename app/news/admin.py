from django.contrib import admin

# Register your models here.
from .models import Category
from .models import News
from .models import Comment

admin.site.register(Category)
admin.site.register(News)
admin.site.register(Comment)

