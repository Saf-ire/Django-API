''' Posts model serializer '''
#Django REST framework
from django.contrib.auth.models import User
from rest_framework import serializers

#Models
from posts.models import Author, Post

class PostModelSerializer(serializers.ModelSerializer):
    ''' Post Model Serializer '''

    class Meta:
        model = Post
        fields = ['pk','image', 'title', 'likes', 'created_at']

class GetAuthorSerializer(serializers.ModelSerializer):
    ''' Get Author username from user model '''

    class Meta:
        model = User
        fields = ['username']

class AuthorModelSerializer(serializers.ModelSerializer):
    ''' Author Model Serializer '''

    author = GetAuthorSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ['author', 'post']
        depth = 1
