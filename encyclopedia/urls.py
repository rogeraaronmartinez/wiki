from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("add/", views.add, name="add"),
    path("error/", views.error, name="error"),
    path("random_entry/", views.random_entry, name="random_entry"),
    path("search/", views.search, name="search"),
    path("edit/<str:title>", views.edit, name="edit")
]
