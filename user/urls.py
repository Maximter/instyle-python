from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('follow/<str:username>/', views.follow),
    path('close/<str:user_id>/', views.toggle_close_friend),
    path('block/<str:user_id>/', views.block_user),
    path('unfollow/<str:username>/', views.unfollow),
    path('<str:username>/', views.user_page),
]
