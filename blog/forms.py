from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from blog.models import Post


class CreatePostForm(forms.ModelForm):
    image = forms.ImageField(label='تصاویر')
    class Meta:
        model = Post
        fields = ['title', 'content', 'reading_time','category']

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label=' Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValidationError('پسورد ها مطابقت ندارد')
        return cd['password2']