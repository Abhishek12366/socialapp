from django.contrib.auth.models import User
from api.models import Friends
from api.models import Posts

def people_list(request, *args, **kwargs):
    people = User.objects.exclude(username=request.user)
    return {'people':people}

def user_followings(request, *args, **kwargs):
    followings = Friends.objects.filter(follower=request.user)
    return {'followings':followings}

def trending_posts(request, *args, **kwargs):
    qs = Posts.objects.all().order_by()
    return qs