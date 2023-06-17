from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_index),
    path('create/', views.create),
]
