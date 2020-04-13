from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("<int:group_id>", views.group, name="group"),
    path("<int:group_id>/submit_post", views.submit_post, name="submit_post"),
    path("login",views.login_display, name="login_display"),
    path("login2",views.login_handler, name="login"),
    path("logout",views.logout_handler, name="logout"),
    path("signup",views.signup_display, name="signup_display"),
    path("signup2",views.signup_handler, name="signup"),
    path("admin_login", views.admin_login_handler, name="admin_login"),
    path("admin_settings", views.admin_settings, name="admin_settings"),
    path("create_group", views.create_group, name="create_group"),
    path("add_users_to_group", views.add_users_to_group, name="add_users_to_group"),
]