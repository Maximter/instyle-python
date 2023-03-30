from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('', views.index),
    path('follow/<str:username>/', views.follow),
    path('unfollow/<str:username>/', views.unfollow),
    path('<str:username>/', views.user_page),
]