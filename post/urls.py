from django.urls import path

from post import views_post_page
from . import views

urlpatterns = [ 
    path('', views.index),
    path('create/', views.create),
    path('like/<str:id_post>/', views_post_page.like_post),
    path('delete/<str:id_post>/', views_post_page.delete_post),
    path('edit/<str:id_post>/', views_post_page.update_post_comment),
    path('comment/<str:id_post>/', views_post_page.send_comment),
    path('edit-comment/<str:id_interaction>/', views_post_page.edit_comment),
    path('delete-comment/<str:id_interaction>/', views_post_page.delete_comment),
    path('<str:id_post>/', views_post_page.post_page),
]
