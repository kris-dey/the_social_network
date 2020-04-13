from django.contrib import admin
from .models import Post, User, Group

admin.site.register(Post)
admin.site.register(Group)
admin.site.register(User)
