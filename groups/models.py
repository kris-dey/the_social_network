from django.db import models
from passlib.hash import pbkdf2_sha256
from django.contrib.auth.models import User as U

class Post(models.Model):
    text = models.CharField(max_length=254)
    author = models.CharField(max_length=64)
    """
    time = models.CharField(max_length=64)
    date = models.CharField(max_length=64)
    """
    def __str__(self):
        return f"{self.text}"

class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=256)
    staff_status = models.BooleanField(default=False)
    admin_logged_in = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username}"

    def authenthicate_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def create_user(self, username2, password):
        user_auth = U.objects.create_user(username=username2, password=password)
        user_auth.save()

class Group(models.Model):
    group_name = models.CharField(max_length=64)
    posts = models.ManyToManyField(Post, related_name="group", null=True)
    members = models.ManyToManyField(User, related_name="group")
    group_encryption_key = models.CharField(max_length=256, default="")

    def __str__(self):
        return f"{self.group_name}"
