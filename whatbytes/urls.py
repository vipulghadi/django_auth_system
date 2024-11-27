
from django.contrib import admin
from django.urls import path,include
from authentication.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('user/', include("users.urls")),
    path('', home_view,name="home"),
    
    
    
]
