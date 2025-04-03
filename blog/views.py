from http.client import HTTPResponse

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView

from blog.forms import CreatePostForm, UserRegisterForm
from blog.models import Post, Image
from django.contrib import messages



# Create your views here.
def home(request):
    return render(request, 'blog/home.html')
def posts_list(request, category=None):
    if category is not None:
        posts = Post.publish.filter(category=category)
    else:
        posts = Post.publish.all()
    return render(request, 'blog/posts_list.html', {'posts': posts, 'category': category})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'


@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(post=post, imag_file=form.cleaned_data['image'])
            # profile
            return redirect('blog:home')
    else:
        form = CreatePostForm()
    return render(request,'forms/create_post.html',{'form':form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(post=post, imag_file=form.cleaned_data['image'])
            # profile
            return redirect('blog:home')
    else:
        form = CreatePostForm(instance=post)
    return render(request,'forms/create_post.html',{'form':form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        # profile
        return redirect('blog:home')
    return render(request, 'forms/delete_post.html',{'post':post})

def profile(request):
    return HttpResponse('profile')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # Account.objects.create(user = user)
            return render(request, 'registration/register_done.html', {'user': user})

    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})