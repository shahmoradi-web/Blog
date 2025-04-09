from django import template
from ..models import Post, Comment, User
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe

register = template.Library()


# custom-template-tags (simple tags)
@register.simple_tag()
def total_posts():
    return Post.publish.count()


@register.simple_tag
def most_discussed_posts(count=4):
    return Post.publish.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_post_data():
    return Post.publish.last().published


@register.simple_tag
def most_reading_time(count=4):
    return Post.publish.order_by('-reading_time')[:count]


@register.simple_tag
def least_reading_time(count=4):
    return Post.publish.order_by('reading_time')[:count]


@register.simple_tag
def active_user(count=3):
    return User.objects.annotate(user_count=Count('user_posts')).order_by('-user_count')[:count]


@register.filter(name='markdown')
def to_markdown(value):
    return mark_safe(markdown(value))
#
#
# @register.filter()
# def censorship(text):
#     censorship_list = ['gav', 'khar', 'avazi', 'fuck']
#     text_split = text.split(' ')
#     text_len = len(text_split)
#     for letter in text_split:
#         if letter in censorship_list:
#             text_split.remove(letter)
#
#     if len(text_split) == text_len:
#         return " ".join(text_split)
#     else:
#         return " ".join(text_split) + ' (contains censored text)'
#
#
#
# custom-template-tags (Inclusion  tags)
@register.inclusion_tag('partials/latest_post.html')
def latest_post(count=4):
    l_posts = Post.publish.order_by('-published')[:count]
    context = {
        'l_posts': l_posts,
    }
    return context

