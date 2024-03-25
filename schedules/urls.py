
from django.urls import path
from .views import shd_home

urlpatterns = [
    path('home-main/', shd_home, name='scd-home'),
    # path('w/', homepage2,name='home-main2'),
]
