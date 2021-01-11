from django.urls import path
from django.conf.urls import url
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("encyclopedia/<str:title>", views.show_entry, name="show_entry"),
    path("newpage", views.new_page, name="newpage"),
    path("search" , views.search , name="search"),
    path("encyclopedia/<str:title>/edit",views.edit , name="edit"),
    path("random", views.random, name="random")
]