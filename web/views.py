from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import redirect, render
from api.models import *
from .forms import *
from django.views.generic import CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def signin_required(fn):
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated:
            return redirect("sign-up")
        else:
            return fn(request, *args, **kw)
    return wrapper

decs = [signin_required]
class UserReigtrationView(CreateView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('sign-up')

    def form_invalid(self, form):
        if form.is_valid():
            messages.success(self.request, 'Account has been created')
        else:
            messages.error(self.request, 'An error occured try again')
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request)
                return render(request, "login.html", {'form':form})

class IndexView(CreateView, ListView):
    template_name = "index.html"
    form_class = PostForm
    model = Posts
    success_url = reverse_lazy("home")
    queryset = Posts.objects.all().order_by('-created_date')
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        return context
    

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user=self.request.user
            messages.success(self.request, "New post has been uploaded")
            return super().form_valid(form)
        else:
            messages.error(self.request, "uploading failed")
            return render(self.request, "index.html", {"form":form})


def add_comment(request, *args, **kwargs):
    id = kwargs.get('id')
    cmt = request.POST.get('comment')
    qs = Posts.objects.get(id=id)
    # Comments.objects.create(comment=cmt, post=qs, user=request.user)
    qs.comments_set.create(user=request.user, comment=cmt)
    messages.success(request, " your has been Comment added succesfully")
    return redirect("home")

def like_post(request, *args, **kwargs):
    id = kwargs.get('id')
    ps = Posts.objects.get(id=id)
    if ps.like.contains(request.user):
        ps.like.remove(request.user)
    else:
        ps.like.add(request.user)
    return redirect("home")

def dislike_post(request, *args, **kwargs):
    id = kwargs.get('id')
    ps = Posts.objects.get(id=id)
    if ps.dislike.contains(request.user):
        ps.dislike.remove(request.user)
    else:
        ps.dislike.add(request.user)
    return redirect("home")

def delete_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            post = Posts.objects.get(id=post_id)
            if request.user == post.user:
                try:
                    delete_post= post.delete()
                    return HttpResponse("post deleted sucessfully")
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse("post deleted sucessfully")
        else:
            return HttpResponse()
    else:
        return HttpResponseRedirect(('login'))

# @csrf_exempt
# def like_post(request, id):
#     if request.user.is_authenticated:
#         if request.method == 'GET':
#             post = Posts.objects.get(pk=id)
#             print(post)
#             try:
#                 post.like.add(request.user)
#                 post.save()
#                 return HttpResponse("U LIKED THE POST")
#             except Exception as e:
#                 return HttpResponse(e)
#         else:
#             return HttpResponse()
#     else:
#         return HttpResponseRedirect(('login'))

# @csrf_exempt
# def dislike_post(request, id):
#     if request.user.is_authenticated:
#         if request.method == 'GET':
#             post = Posts.objects.get(pk=id)
#             print(post)
#             try:
#                 post.like.remove(request.user)
#                 post.save()
#                 return HttpResponse("U DISLIKED THE POST")
#             except Exception as e:
#                 return HttpResponse(e)
#         else:
#             return HttpResponse()
#     else:
#         return HttpResponseRedirect(('login'))



class ListPeopleView(ListView):
    template_name="people/list_people.html"
    model = User
    context_object_name = 'people'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        context["posts"] = Posts.objects.all().order_by('-created_date')
        return context
    

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)
 

def add_follower(request, *args, **kwargs):
    id = kwargs.get('id')
    usr = User.objects.get(id=id)
    if not Friends.objects.filter(user=usr, follower=request.user):
        Friends.objects.create(user=usr, follower=request.user)
    else:
        Friends.objects.get(user=usr, follower=request.user).delete()
    return redirect("people")

@signin_required
def profile(request):
    mypost=Posts.objects.filter(user_id=request.user)
    postcount=Posts.objects.filter(user_id=request.user).count

    mydetails=User.objects.filter(id=request.user.id)
    # follower_count = Friends.objects.filter(id=request.user.id).follower.all().count()
    # following_count = Friends.objects.filter(id=request.user.id).count()

    context={
        'mydetails':mydetails,'mypost':mypost,'postcount':postcount,

    }
    return render(request, 'profile/profile2.html', context)


def sign_out(request, *args, **kwargs):
    login(request, request.user)
    return redirect("sign-in")


def search(request):
    query = request.GET.get('user')
    users = User.objects.filter(username=query)
    return render(request, 'search_results.html', {'users': users})


# def profile2(request, username):
#     user = User.objects.get(username=username)
#     all_posts = Posts.objects.filter(user_id=request.user)
#     page_number = request.GET.get('page')
#     if page_number == None:
#         page_number = 1
#     posts = Posts.objects.filter(user_id=request.user).count
#     followings = []
#     suggestions = []
#     follower = False
#     if request.user.is_authenticated:
#         followings = Friends.objects.filter(follower=request.user).values_list('user', flat=True)
#         suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]

#         if request.user in Friends.objects.get(user=user).follower.all():
#             follower = True
    
#     follower_count = Friends.objects.get(user=user).follower.all().count()
#     following_count = Friends.objects.filter(followers=user).count()
#     return render(request, 'profileview.html', {
#         "username": user,
#         "posts": posts,
#         "posts_count": all_posts.count(),
#         "suggestions": suggestions,
#         "page": "profile",
#         "is_follower": follower,
#         "follower_count": follower_count,
#         "following_count": following_count
#     })
