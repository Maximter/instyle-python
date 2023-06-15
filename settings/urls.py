from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('edit-profile', views.edit_profile),
    path('change-avatar', views.change_avatar),
    path('favorite/<str:id_user>/', views.favorite),
    path('change-privacy', views.change_privacy),
    path('change-password', views.change_password),
    path('forgot-password', views.forgot_password),
    path('delete', views.delete_user),
]
