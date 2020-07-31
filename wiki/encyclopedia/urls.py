from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("delete", views.delete, name="delete"),
    path("del/<str:name>", views.delcontent, name="del"),
    path("random", views.random, name="random"),
    path("search", views.search, name = "search"),
    path("<str:name>", views.wiki, name="wiki"),
    path("<str:name>", views.error, name="other_error"),
] 
