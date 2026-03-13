from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following/", views.following, name="following"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_post, name="create_post"),
    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
]