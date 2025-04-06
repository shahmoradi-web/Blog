from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from blog.models import Post, Comment, Account


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class TicketForm(forms.Form):
    message = forms.CharField(required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isdigit():
                raise forms.ValidationError("شماره تلفن فقط باید شامل عدد باشد")
            else:
                return phone


class SearchForm(forms.Form):
    query = forms.CharField()


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountEditForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['data_of_brith', 'bio', 'photo', 'job']
