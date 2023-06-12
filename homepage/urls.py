from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('get-recommendation', views.get_recommendation),
]
