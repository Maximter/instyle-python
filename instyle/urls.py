from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls')),
    path('login/', include('login.urls')),
    path('signup/', include('signup.urls')),
    path('user/', include('user.urls')),
    path('post/', include('post.urls')),
    path('settings/', include('settings.urls')),
    path('recommendation/', include('recommendation.urls')),
    path('notification/', include('notification.urls')),
]
