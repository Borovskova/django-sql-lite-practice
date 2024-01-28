from . import views
from django.urls import path, re_path

urlpatterns = [
    path("list", views.getCarsList, name="cars"),
    path("", views.actionWithCar),
    path("<str:id>", views.actionWithCar),
]
