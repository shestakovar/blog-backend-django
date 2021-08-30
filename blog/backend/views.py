from django.shortcuts import render

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

from rest_framework import viewsets


class PostAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(origin=self.kwargs['post_pk'])
