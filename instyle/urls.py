from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('homepage.urls')), 
    path('login/', include('login.urls')),  
    path('signup/', include('signup.urls')), 
    path('user/', include('user.urls')), 
    path('post/', include('post.urls')), 
    path('settings/', include('settings.urls')), 
    # path('admin/', admin.site.urls),
]
