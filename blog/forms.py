from django import forms
from django.contrib.auth.models import User

from blog.models import Post


class CreatePostForm(forms.ModelForm):
    image = forms.ImageField(label='تصاویر')
    class Meta:
        model = Post
        fields = ['title', 'content', 'reading_time','category']