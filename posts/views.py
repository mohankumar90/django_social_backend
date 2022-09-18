from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import mail

from posts.models import *
from posts.seriealizer import *

from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions

import json
import datetime

# from rest_framework import status
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.response import Response
# Create your views here.

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class =  personSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class =  postsSerializer

    def retrieve(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post = postsSerializer(post).data
        person = Person.objects.get(id=post["owner"])
        post["owner"] = {
                            "person_id": person.id,
                            "person_name": person.user.username,
                            "person_pic": person.pic,
                        }
        return HttpResponse(json.dumps(post), content_type="application/json")

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class =  commentSerializer

class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class =  likesSerializer

@csrf_exempt
def signup(request):
    if request.user.is_authenticated:
        return HttpResponse(json.dumps({
            "status": False,
            "data": {
                    "userid": request.user.id,
                    "firstname": request.user.first_name,
                    "email": request.user.email
                }
            }), content_type="application/json")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        pic = request.POST.get('pic')

        if not (username and password and first_name and email):
            return HttpResponse(json.dumps({
                "status": False,
                "data": {
                    "error": "some parameters are missing"
                }
            }), content_type="application/json")

        u, created = User.objects.get_or_create(username=username, password=password, email=email, first_name=first_name)
        
        if created:
            obj = Person(user=u, country=country, pic=pic)
            obj.save()
        return HttpResponse(json.dumps({
            "status": created,
            "data": u.id
        }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "status": False
        }), content_type="application/json")

@csrf_exempt    
def loginRequest(request):
    if request.method == 'POST':
        username = request.POST.get('un')
        password = request.POST.get('pw')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps({
                "status": True, 
                "data": {
                    "userid": user.id,
                    "firstname": user.first_name,
                    "email": user.email
                }
                }), content_type="application/json")
        else:
            return HttpResponse(json.dumps({
                "status": False,
                "data": {
                    "error": "No user found or not able to authenticate"
                }
            }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "data": {}
            }), content_type="application/json")

@csrf_exempt
def logoutRequest(request):
    logout(request)
    return HttpResponse(json.dumps({
        "status": True,
    }), content_type="application/json")


@csrf_exempt
def createPost(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        userid = request.POST.get('userid')
        
        if not (title and desc and userid):
            return HttpResponse(json.dumps({
            "status": False,
            "data": {
                "error": "params missing or userid not found"
            }
            }), content_type="application/json")
        
        owner = Person.objects.get(user=User.objects.get(id=userid))
        obj = Post(title=title, desc=desc, created=datetime.datetime.now(), owner=owner)
        obj.save()
        return HttpResponse(json.dumps({
            "status": True
            }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "data": {
                "error": "not allowed with get method"
            }
            }), content_type="application/json")
    
@csrf_exempt
def like(request):
    if request.method == "POST":
        person = request.POST.get('person')
        post = request.POST.get('post')

        if not (person and post):
            return HttpResponse(json.dumps({
            "status": False,
            "data": {
                "error": "params missing"
            }
            }), content_type="application/json")

        person = Person.objects.get(id=person)
        post = Post.objects.get(id=post)

        Likes.objects.get_or_create(person=person, post=post)

        return HttpResponse(json.dumps({
            "status": True,
            "data": {
                "likes": Likes.objects.filter(post=post).count()
            }
            }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "data": {
                "error": "not allowed with get method"
            }
            }), content_type="application/json")

@csrf_exempt
def comment(request):
    if request.method == "POST":
        cmd = request.POST.get('cmd')
        userid = request.POST.get('userid')
        post = request.POST.get('post')

        if not (cmd and userid and post):
            return HttpResponse(json.dumps({
            "status": False,
            "data": {
                "error": "params missing"
            }
            }), content_type="application/json")
        
        owner = Person.objects.get(id=userid)
        post = Post.objects.get(id=post)

        if owner and post:
            obj = Comment(cmd=cmd, owner=owner, post=post)
            obj.save()
            return HttpResponse(json.dumps({
                "status": True
                }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "status": False,
            "data": {
                "error": "not allowed with get method"
            }
            }), content_type="application/json")

@csrf_exempt
def sendNotifications(request):

    persons = Person.objects.all()

    for person in persons:
        toMail = person.user.email
        noOfPosts = Post.objects.filter(owner=person).count()
        noOfLikes = Likes.objects.filter(person=person).count()
        noOfCmds = Comment.objects.filter(owner=person).count()

        body = "Posts: " + str(noOfPosts) + "\nLikes: " + str(noOfLikes) + "\nComments: " + str(noOfCmds)

        with mail.get_connection() as connection:
            mail.EmailMessage(
                "taskSub: Notification", body, "billamohan90@yahoo.in", [toMail],
                connection=connection,
            ).send()

        break

    return HttpResponse(json.dumps({
            "status": True,
            "data": {
                "error": "dd"
            }
            }), content_type="application/json")

@csrf_exempt
def listOfPosts(request):
    if request.method == "POST":
        personId = request.POST.get('personId')

        if not (personId):
            return HttpResponse(json.dumps({
            "status": False,
            "data": {
                "error": "params missing"
            }
            }), content_type="application/json")
        else:
            objs = Post.objects.filter(owner=personId)
            person = Person.objects.get(id=personId)
            returnable = []
            for i in objs:
                returnable.append(postsSerializer(i).data)
            return HttpResponse(json.dumps({
                "status": True,
                "data": {
                    "person_name": person.user.username,
                    "person_pic": person.pic,
                    "postData": returnable
                }
            }), content_type="application/json")
    return HttpResponse(json.dumps({
            "status": False,
            "data": {
                "error": "no get method allowed"
            }
            }), content_type="application/json")

@csrf_exempt
def getCommentsForPost(request, postId):
    if postId:
        comments = Comment.objects.filter(post=postId).values("id", "cmd", "owner")
        returnable = []
        for cmd in comments:
            person = Person.objects.get(id=cmd["owner"])
            person = {"id": person.id, "person_name": person.user.username, "person_pic": person.pic}
            returnable.append({"id": cmd["id"], "cmd": cmd["cmd"], "owner": person})
        # comments = list(comments)
        return HttpResponse(json.dumps(returnable), content_type="application/json")
