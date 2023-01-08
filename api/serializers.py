from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    # profile_pic = serializers.ImageField(upload_to='images')
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            # "profile_pic"
        ]
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class CommentSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    created_date = serializers.CharField(read_only=True)
    class Meta:
        model = Comments
        fields = [
            "user",
            "comment",
            "created_date",
        ]

    def create(self, validated_data):
        user = self.context.get('user')
        post = self.context.get('post')
        return post.comments_set.create(user=user, **validated_data)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    likes = serializers.CharField(read_only=True)
    dislikes=serializers.CharField(read_only=True)
    comment = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Posts
        fields = [
            "user",
            "title",
            "image",
            "likes",
            "dislikes",
            "comment",
        ]
    