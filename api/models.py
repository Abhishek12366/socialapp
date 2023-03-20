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
    liked=models.ManyToManyField(User,related_name="likes",null=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment

    @property
    def likecounts(self):
        return self.liked.all().count()
class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    date = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
      bio = models.TextField(max_length=500,default="no bio", blank=True)
      following = models.ManyToManyField(User, related_name='following', blank=True)


def __str__(self):
        return f'Profile for user {self.user.username}'