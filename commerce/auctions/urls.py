from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings", views.my_listings, name="listings"),
    path("profile", views.update_personal_info, name="profile_info"),
    path("profile/<str:name>", views.get_profile_info, name="profile"),
    path("bid/<str:name>", views.bid, name="bid"),
    path("bid", views.view_error, name="bid"),
    path("bid/", views.view_error, name="bid"),
    path("bid/login", views.login_view, name="login"),
    path("bid/login/", views.login_view, name="login"),
    path("bid/login/<str:name>", views.login_view, name="login"),
    path("login/", views.login_view, name="login_with_extra_info"),
    path("login/<str:name>", views.login_view, name="login_with_extra_info"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("view", views.view_error, name='view_error'),
    path("view/", views.view_error, name='view_error'),
    path("view/<str:name>", views.view, name='view'),
    path("delete", views.view_error, name="delete"),
    path("delete/", views.view_error, name="delete"),
    path("delete/<str:name>", views.delete, name="delete"),
    path("delete/login", views.login_view, name="login"),
    path("delete/login/", views.login_view, name="login"),
    path("detele/login/<str:name>", views.login_view, name="login"),
    path("search", views.search, name="search")
]
