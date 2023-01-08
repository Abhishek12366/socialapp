from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserReigtrationView.as_view(), name="sign-up"),
    path("" ,LoginView.as_view(), name="sign-in"),
    path("logout/", sign_out, name="sign-out"),
    path("index/", IndexView.as_view(), name="home"),
    path("people/", ListPeopleView.as_view(), name="people"),
    path("post/<int:id>/comment/add", add_comment, name="add-comment"),
    path("post/<int:id>/like/add", like_post, name="like-post"),
    path("post/<int:id>/like/add", dislike_post, name="dislike-post"),
    path("user/<int:id>/follower/add", add_follower, name="add-follower"),
    path("myprofile/",profile, name="myprofile"),
]