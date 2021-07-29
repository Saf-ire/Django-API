''' Post ViewSet '''

#Django REST framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

#Permissions
from rest_framework import permissions
from posts.permissions import IsAuthor

#Models
from posts.models import Post, Author

#Serializers
from posts.serializers import PostModelSerializer, AuthorModelSerializer

class PostViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    ''' Post Model ViewSet '''

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    def get_permissions(self):
        ''' Asign Permissions base on action '''
        permissions = [IsAuthenticated]

        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsAuthor)
        
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        ''' Save the author of the post '''
        post = serializer.save()
        author = self.request.author
        Author.objects.create(author=author, post=post)

    def retrieve(self, request, *args, **kwargs):
        ''' Bring the data of the post with its author '''

        instance = self.get_object()
        author = Author.objects.get(post = instance.pk)
        serializer = AuthorModelSerializer(author)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        ''' List All the posts data with the authors' '''

        queryset = Author.objects.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = AuthorModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = AuthorModelSerializer(queryset, many=True)
        return Response(serializer.data)

    






