from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserReigtrationView.as_view(), name="sign-up"),
    path("" ,LoginView.as_view(), name="sign-in"),
    path("logout/", sign_out, name="sign-out"),
    path('comments/<int:pk>/delete/', delete_comment, name='delete_comment'),
    path("index/", IndexView.as_view(), name="home"),
    path("people/", ListPeopleView.as_view(), name="people"),
    path("post/<int:id>/comment/add", add_comment, name="add-comment"),
    path("n/post/<int:post_id>/delete",delete_post, name="deletepost"),
    path("post/<int:id>/like/add", like_post, name="like-post"),
    path('posts/<int:pk>/unlike/', unlike_post, name='unlike_post'),
    path("user/<int:id>/follower/add", add_follower, name="add-follower"),
    path("myprofile/",profile, name="myprofile"),
    # path('profile/', profile2,name='profile'),
    path('posts/<int:pk>/like/',like_post, name='like_post'),
    # path('search/', search, name='search'),
    #  path('search', search, name='search'),
    path('comments/<int:pk>/like/',like_comment, name='like_comment'),
    path('comments/<int:pk>/unlike/',unlike_comment, name='unlike_comment'),
]