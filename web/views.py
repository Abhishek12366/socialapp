from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from api.models import *
from .forms import *
from django.views.generic import CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
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
                messages.error(request, "Your credentials not matching, try again")
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
    messages.success(request, "Comment added succesfully")
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


    context={
        'mydetails':mydetails,'mypost':mypost,'postcount':postcount

    }
    return render(request, 'profile/profile2.html', context)


def sign_out(request, *args, **kwargs):
    login(request, request.user)
    return redirect("sign-in")