from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="login"),
    path("signUp", views.signUp, name="signUp"),
    path("logout", views.logout_view, name="logout"),
    path("delete_details", views.delete_details, name="delete_details"),
    # API VIEW
    path("edit_details", views.edit_details, name="edit_details"),
]