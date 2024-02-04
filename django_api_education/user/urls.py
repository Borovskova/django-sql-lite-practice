from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.action_with_user),
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path("list", views.get_users_list, name="users"),
    path("<str:id>", views.action_with_user),
]
