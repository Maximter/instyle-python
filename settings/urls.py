from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('edit-profile', views.edit_profile),
]
