
from django.urls import path
from .views import shd_home,post_shd
from .views import download_shd

urlpatterns = [
    path('home-main/', shd_home, name='scd-home'),
    path('shd-for-workCenter/',post_shd),
    path('home-main/download/',download_shd)
]
