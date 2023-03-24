from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    #  path('<int:pk>/', views.icecream_detail),
]
