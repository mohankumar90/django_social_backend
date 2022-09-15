from django.urls import path

from . import views
# from rest_framework import routers

app_name = 'posts'

urlpatterns = [
    path('signup', views.signup),
    path('login', views.loginRequest),
    path('logout', views.logoutRequest),
    path('createPost', views.createPost),
    path('like', views.like),
    path('comment', views.comment),
    path('sendNotifications', views.sendNotifications),
]