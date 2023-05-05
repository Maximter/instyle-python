from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('yandex/', views.yandex),
    path('confirm/', views.confirm),
    path('change-forgot-password-page/', views.forgot_password_page),
    path('change-password/', views.change_password),
]
