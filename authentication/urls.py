
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_view,name="signup"),
    path('login/', login_view,name="login"),
    path('logout/', logout_view,name="logout"),
    path('reset-password/', reset_password_view,name="reset-password"),
    path('forgot-password/', forget_password_view,name="forgot-password"),
    
]