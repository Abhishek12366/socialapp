from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.

class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PostView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["Post"], detail=True)
    def add_comment(self, request, *args, **kwargs):

        post = self.get_object()
        user = request.user

        serializer = CommentSerializer(data=request.data, context={"post":post, "user":user})

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    
    @action(methods=["GET"], detail=True)
    def add_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        post.like.add(user)
        return Response("liked")

    @action(methods=["GET"], detail=True)
    def add_dislike(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        post.dislike.add(user)
        return Response("liked")