from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    like = models.ManyToManyField(User, related_name='like')
    dislike=models.ManyToManyField(User, related_name='dislike')
    created_date = models.DateField(auto_now_add=True)

    @property
    def likes(self):
        return self.like.all().count()

    @property
    def dislikes(self):
        return self.dislike.all().count()

    @property
    def comments(self):
        return self.comments_set.all()


    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ""

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    created_date = models.DateField(auto_now_add=True)

class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    date = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"
        