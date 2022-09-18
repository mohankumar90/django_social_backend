from .models import *
from rest_framework import serializers

class postsSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField("get_likes")
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'desc', 'created', 'owner', 'likes')
    
    def get_likes(self, obj):
        l = Likes.objects.filter(post=obj.id).count()
        return l

class personSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'

class commentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'cmd', 'owner', 'post')

class likesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = '__all__'