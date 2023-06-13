from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('send/', views.send_message_view,),
    path('get-messages/<str:id_user>', views.get_messages,),
]
