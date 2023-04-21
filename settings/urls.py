from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('edit-profile', views.edit_profile),
    path('change-avatar', views.change_avatar),
    path('change-password', views.change_password),
    path('delete', views.delete_user),
]
