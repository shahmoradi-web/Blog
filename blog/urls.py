from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts_list, name='posts_list'),
    path('posts/detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('posts/<str:category>', views.posts_list, name='posts_list_category'),
    # path('profile/create-post/<int:post_id>', views.edit_post, name='edit_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/create-post', views.create_post, name='create_post'),
    path('profile/create-post/<int:pk>', views.edit_post, name='edit_post'),
    path('profile/delete-post/<int:pk>', views.delete_post, name='delete_post'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done/'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password_reset/complete'),
         name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register/', views.register, name='register'),
    path('posts/<int:post_id>/comment', views.post_comment, name='post_comment'),
    path('post/comments/<int:post_id>', views.comments_show, name='comments_show'),

    path('ticket', views.ticket, name='ticket'),
    path('search/', views.post_search, name='post_search'),
    path('profile', views.profile, name='profile'),
    path('profile/show/<int:user_profile>', views.profile_show, name='profile_show'),
    path('account/edit', views.edit_account, name='edit_account'),

]

