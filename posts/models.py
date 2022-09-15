from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    country = models.CharField(max_length=50, db_column="country")
    pic = models.CharField(max_length=250, db_column="pic")

class Post(models.Model):
    title = models.CharField(max_length=150, db_column="title")
    desc = models.CharField(max_length=1000, db_column="desc")
    created = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, db_column="owner")
    
    class Meta:
        ordering = ["title"]

class Comment(models.Model):
    cmd = models.CharField(max_length=1000, db_column="cmd")
    owner = models.ForeignKey(Person, on_delete=models.CASCADE, db_column="owner")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column="post", default=None)

class Likes(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, db_column="person")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column="post")