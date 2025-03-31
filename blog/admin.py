from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django_jalali.admin.filters import JDateFieldListFilter

from .models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'status']
    list_filter = ['status', ('published', JDateFieldListFilter)]
    ordering = ['-published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'imag_file']
