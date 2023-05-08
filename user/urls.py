from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('follow/<str:username>/', views.follow),
    path('unfollow/<str:username>/', views.unfollow),
    path('<str:username>/', views.user_page),
]
