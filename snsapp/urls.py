from django.urls import path
from .views import Home, MyPost, CreatePost, DetailPost, UpdatePost, DeletePost, LikeHome, LikeDetail, LikeProfile, FollowHome, FollowDetail, FollowProfile, FollowList, Profile, UpdateProfile


app_name = 'snsapp'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('mypost/', MyPost.as_view(), name='mypost'),
    path('create/', CreatePost.as_view(), name='create'),
    path('detail/<int:pk>', DetailPost.as_view(), name='detail'),
    path('detail/<int:pk>/update', UpdatePost.as_view(), name='update'),
    path('detail/<int:pk>/delete', DeletePost.as_view(), name='delete'),
    path('like-home/<int:pk>', LikeHome.as_view(), name='like-home'),
    path('like-detail/<int:pk>', LikeDetail.as_view(), name='like-detail'),
    path('like-profile/<int:pk>', LikeProfile.as_view(), name='like-profile'),
    path('follow-home/<int:pk>', FollowHome.as_view(), name='follow-home'),
    path('follow-detail/<int:pk>', FollowDetail.as_view(), name='follow-detail'),
    path('follow-profile/<slug:username>', FollowProfile.as_view(), name='follow-profile'),
    path('follow-list', FollowList.as_view(), name='follow-list'),
    path('profile/<slug:username>', Profile.as_view(), name='profile'),
    path('profile/<int:pk>/update', UpdateProfile.as_view(), name='profile-update'),
]