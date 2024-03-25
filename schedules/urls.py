
from django.urls import path
from .views import shd_home,post_shd

urlpatterns = [
    path('home-main/', shd_home, name='scd-home'),
    path('shd-for-workCenter/',post_shd)
]
