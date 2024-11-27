
from django.urls import path,include
from .views import user_profile

urlpatterns = [
path('my-profile/', user_profile,name="my-profile"),

]