from django.urls import path

from post import views_post_page
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('get_vk_token/', views.get_vk_token),
    path('get_vk_photos/', views.get_vk_photos),
    path('like/<str:id_post>/', views_post_page.like_post),
    path('delete/<str:id_post>/', views_post_page.delete_post),
    path('edit/<str:id_post>/', views_post_page.update_post_comment),
    path('comment/<str:id_post>/', views_post_page.send_comment),
    path('edit-visibility/<str:id_post>/', views_post_page.edit_visibility),
    path('hide-like/<str:id_post>/', views_post_page.hide_like),
    path('add-favorite/<str:id_post>/', views_post_page.add_favorite),
    path('hide-comment/<str:id_post>/', views_post_page.hide_comment),
    path('edit-comment/<str:id_interaction>/', views_post_page.edit_comment),
    path('delete-comment/<str:id_comment>/', views_post_page.delete_comment),
    path('<str:id_post>/', views_post_page.post_page),
]
