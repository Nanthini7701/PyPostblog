from django.urls import path
from . import views
from .views import profile_view, settings_view
app_name = "blog"

urlpatterns = [
    path("home/", views.post_list, name="home"),
    path("", views.post_list, name="post_list"),
    path("posts/new/", views.post_create, name="post_create"),
    path("posts/<slug:slug>/", views.post_detail, name="post_detail"),
    path("posts/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("posts/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("posts/<slug:slug>/like/", views.post_like, name="post_like"),
    path("accounts/register/", views.register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("settings/", settings_view, name="settings"),
]
