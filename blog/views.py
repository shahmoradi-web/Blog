from http.client import HTTPResponse

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.postgres.search import TrigramSimilarity
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from blog.forms import CreatePostForm, UserRegisterForm, CommentForm, TicketForm, SearchForm
from blog.models import Post, Image, Comment, Ticket
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


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm()
    comments = Comment.objects.filter(post=post_id)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }

    return render(request, 'blog/post_details.html', context)


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

@login_required
def profile(request):
    user = request.user
    posts = Post.publish.filter(author=user)
    post_count = posts.count()
    if post_count > 10:
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.get_page(page_number)
        except EmptyPage:
            posts = paginator.get_page(paginator.num_pages)
        except PageNotAnInteger:
            posts = paginator.get_page(1)

    return render(request, 'blog/profile.html', {'posts': posts, 'post_count': post_count})


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



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.name = request.user
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'forms/comment.html', context)


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message=cd.get('message'), name=request.user,
                                  email=cd.get('email'), phone=cd.get('phone'),
                                  subject=cd.get('subject'))
            return redirect('blog:profile')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})

def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result1 = (Post.objects.annotate(similarity=TrigramSimilarity('title', query))
                       .filter(similarity__gte=0.1))
            result2 = (Post.objects.annotate(similarity=TrigramSimilarity('content', query))
                       .filter(similarity__gte=0.1))
            from itertools import chain
            results = list(chain(result1, result2))

            # sort_results

            new_results = []
            while results:
                max_simi = results[0].similarity
                max_object = results[0]
                for result in results:
                    if result.similarity > max_simi:
                        max_simi = result.similarity
                        max_object = result
                new_results.append(max_object)
                results.remove(max_object)
            results = new_results

    context = {
        'results': results,
        'query': query,
        'len_results' : len(results)
    }
    return render(request, 'blog/search.html', context)


def comments_show(request, post_id):
    comments = Comment.objects.filter(post = post_id)
    return render(request, 'blog/comments_show.html', {'comments': comments})
