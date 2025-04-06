from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django_jalali.admin.filters import JDateFieldListFilter

from .models import *
# Register your models here.

class ImagInline(admin.TabularInline):
    model = Image
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['name', 'body', 'active']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'status']
    list_filter = ['status', ('published', JDateFieldListFilter)]
    ordering = ['-published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status']
    inlines = [ImagInline, CommentInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'imag_file']

@admin.register(Comment)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'body', 'created']

@admin.register(Ticket)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['data_of_brith', 'bio', 'photo', 'job']