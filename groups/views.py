from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from passlib.hash import pbkdf2_sha256
from cryptography.fernet import Fernet
import base64

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

    user_logged_in = True

    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        raise Http404("No such group exist.")

    member_in_group = False
    
    for member in group.members.all():
        if request.user.username == member.username:
            member_in_group = True
            break
    
    # if not member_in_group:
    #     return render(request, "homepage.html", {"message": "Sorry, you must be a member of the group to access the page.", "user_logged_in": user_logged_in})

    posts = group.posts.all()
    if member_in_group:
        deciphered_posts = []
        decipherer = Fernet(group.group_encryption_key.encode())
        
        for post in posts:
            post_text = str(decipherer.decrypt(post.text.encode()), 'utf-8')
            post = {
                "text": post_text,
                "author": post.author,
            }
            deciphered_posts.append(post)
        posts = deciphered_posts

    context = {
        "group": group,
        "posts": posts,
        "members": group.members.all(),
        "member_in_group": member_in_group,
    }
    return render(request, "group.html", context)

def submit_post(request, group_id):

    if not request.user:
        return render(request, "login.html", {"message": "Please log in before making a post please."})

    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        raise Http404("No such group exist.")
 
    user_in_group = False
    for member in group.members.all():
        if member.username == request.user.username:
            user_in_group = True
        
    if user_in_group:
        post_text = request.POST["post_text"]

        decipherer = Fernet(group.group_encryption_key.encode())
        ciphered_text = decipherer.encrypt(bytes(post_text, 'utf-8'))

        post = Post(text=ciphered_text.decode(), author=request.user.username)
        post.save()
        post.group.add(group)
        post.save()
    else:
        return render(request, "index.html", {"message": "You must be a member of the group to make a post, sorry."})

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
    #request.user.admin_logged_in = False
    #request.user.save()
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

def admin_login_handler(request):
    if request.method =='POST':

        username = request.POST.get("username2", "")
        password = request.POST.get("password", "")
        
        try:
            user = User.objects.filter(username=username)
        except Group.DoesNotExist:
            raise Http404("No such user exist.")

        if not user:
            return render(request, "admin_login.html", {"message": "Incorrect username or password."})

        legit_user = user[0].authenthicate_password(password=password)

        if(not user[0].staff_status):
            return render(request, "admin_login.html", {"message": "User not an admin."})

        if legit_user:
            user_auth = authenticate(request, username=username, password=password)
            login(request, user_auth)
            request.user.admin_logged_in = True
            request.user.save()
            context = {
                "groups": Group.objects.all(),
                "user": request.user,
                "admin_logged_in": request.user.admin_logged_in,
            }
            return render(request,'index.html', context)
            #return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "admin_login.html", {"message": "Invalid credentials."})
             
    else:
        return render(request,'admin_login.html')

def admin_settings(request):
    return render(request,'admin_settings.html')

def create_group(request):
    if request.method =='POST':
        new_group_name = request.POST.get("new_group_name", "")
        encryption_key = Fernet.generate_key().decode()
        new_group = Group(group_name=new_group_name, group_encryption_key=encryption_key)
        new_group.save()
        user = User.objects.filter(username=request.user.username)
        new_group.members.add(user[0])
        new_group.save()
        
        return render(request,'admin_settings.html', {"message":"New group has been created!"})
    else:
        return render(request,'admin_settings.html')

def add_users_to_group(request):
    if request.method =='POST':
        username = request.POST.get("username", "")
        group_name = request.POST.get("group_name", "")

        try:
            user = User.objects.filter(username=username)
        except Group.DoesNotExist:
            raise Http404("No such user exists.")

        try:
            group = Group.objects.filter(group_name=group_name)
        except Group.DoesNotExist:
            raise Http404("No such group exists.")
        
        group[0].members.add(user[0])
        group[0].save()
        
        message = "User '" + username + "' has been added to group '" + group_name + "'!"
 
        return render(request,'admin_settings.html', {"message":message})
    else:
        return render(request,'admin_settings.html')