from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from passlib.hash import pbkdf2_sha256

from .models import Group, Post, User

def index(request):
    if not request.user.is_authenticated:
        return render(request, "homepage.html")

    context = {
        "groups": Group.objects.all(),
        "user": request.user
    }
    return render(request, "index.html", context)

def group(request, group_id):

    if not request.user.is_authenticated:
        return render(request, "homepage.html", {"message": "Please log in or sign up to access a group page."})

    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        raise Http404("No such group exist.")

    context = {
        "group": group,
        "posts": group.posts.all(),
        "members": group.members.all()
    }
    return render(request, "group.html", context)

def submit_post(request, group_id):

    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        raise Http404("No such group exist.")

    post_text = request.POST["post_text"]
    post = Post(text=post_text, author=request.user.username)
    post.save()
    post.group.add(group)
    post.save()

    return redirect("/" + str(group_id))
    #return HttpResponseRedirect(reverse("group", kwargs={'group_id':1}))

def login_display(request):
    return render(request, "login.html")

def login_handler(request):
    username = request.POST.get("username2", "")
    password = request.POST.get("password", "")
    
    try:
        user = User.objects.filter(username=username)
    except Group.DoesNotExist:
        raise Http404("No such user exist.")

    if not user:
        return render(request, "login.html", {"message": "Incorrect username or password."})

    legit_user = user[0].authenthicate_password(password=password)

    if True:
        user_auth = authenticate(request, username=username, password=password)
        login(request, user_auth)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html", {"message": "Invalid credentials."})

def logout_handler(request):
    logout(request)
    return render(request, "homepage.html", {"message": "Logged out."})

def signup_display(request):
    return render(request, "signup.html")

def signup_handler(request):
    username2 = request.POST.get("username", "")
    password = request.POST.get("password", "")

    encrypted_password = pbkdf2_sha256.encrypt(password, salt_size=32, rounds=12000)

    user = User(username=username2, password=encrypted_password)
    user.save()

    user.create_user(username2=username2, password=password)

    return render(request, "login.html", {"message": "Account created. Please log in."})





