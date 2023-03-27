from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index),
    path('create/', views.create),
    path('like/<str:id_post>/', views.like_post),
    path('<str:id_post>/', views.post_page),
    path('delete/<str:id_post>/', views.delete_post),
]
