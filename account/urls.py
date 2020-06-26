from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("user", views.user, name="user"),
    path("logout", views.logout, name="logout"),
]

