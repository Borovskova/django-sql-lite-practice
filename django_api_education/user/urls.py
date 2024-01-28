from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.actionWithUser),
    path("list", views.getUsersList, name="users"),
    path("<str:id>", views.actionWithUser),
]
