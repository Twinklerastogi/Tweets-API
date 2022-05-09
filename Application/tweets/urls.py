from django.db import router
from rest_framework import routers
from django.urls import path
from . import views

urlpatterns = [
    # path('all/tweets', views.TweetList.as_view()),
    path('users/', views.UsersList.as_view()),
    path('tweets/', views.TweetsDetails.as_view()),
    path('tweets/<int:id>/', views.TweetsDetails.as_view()),
    path('alltweets/', views.TweetList.as_view()),
    ]



