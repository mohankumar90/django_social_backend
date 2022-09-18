from django.urls import path
from rest_framework import routers
from . import views
# from rest_framework import routers

app_name = 'posts'

router = routers.DefaultRouter()
router.register(r'Person', views.PersonViewSet)
router.register(r'Post', views.PostViewSet)
router.register(r'Comment', views.CommentViewSet)
router.register(r'Likes', views.LikesViewSet)

urlpatterns = [
    path('signup', views.signup),
    path('login', views.loginRequest),
    path('logout', views.logoutRequest),
    path('createPost', views.createPost),
    path('like', views.like),
    path('comment', views.comment),
    path('sendNotifications', views.sendNotifications),
    path('listOfPosts', views.listOfPosts),
    path('getCommentsForPost/<int:postId>', views.getCommentsForPost),
]

urlpatterns += router.urls