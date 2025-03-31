from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts_list, name='posts_list'),
    path('posts/details/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<str:category>', views.posts_list, name='posts_list_category'),
    # path('profile/create-post/<int:post_id>', views.edit_post, name='edit_post'),
    path('profile/create-post', views.create_post, name='create_post'),
    path('profile/create-post/<int:pk>', views.edit_post, name='edit_post'),
    path('profile/delete-post/<int:pk>', views.delete_post, name='delete_post'),

]

