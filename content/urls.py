from . import views
from django.urls import path

# Create a post/ Update a post
# upload Media
# View the post - feed , post detail

# Every image/video is uploaded individually using upload media end point
# The post object is create with no media/caption because it is needed as reference

urlpatterns = [
    path('', views.UserPostCreateFeed.as_view(), name='user_post_view'),
    path('media/', views.PostMediaView.as_view(), name='post_media')

]