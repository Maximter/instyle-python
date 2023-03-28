from django.urls import path

from post import views_post_page
from . import views

urlpatterns = [ 
    path('', views.index),
    path('create/', views.create),
    path('like/<str:id_post>/', views_post_page.like_post),
    path('delete/<str:id_post>/', views_post_page.delete_post),
    path('edit/<str:id_post>/', views_post_page.update_post_comment),
    path('<str:id_post>/', views_post_page.post_page),
]
