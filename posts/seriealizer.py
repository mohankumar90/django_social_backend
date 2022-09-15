from .models import *
from rest_framework import serializers

class postsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

class personSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'