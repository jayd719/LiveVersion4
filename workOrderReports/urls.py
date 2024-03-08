"""
URL configuration for LiveVersion4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import addToLive,removeFormLive,updateDate,notEnoughPerm,clockedIn


urlpatterns = [
    path('addtolive/', addToLive, name='addtolive'),
    path('removeformlive/', removeFormLive, name='removefromlive'),
    path('upadtedate/', updateDate, name='updatedate'),
    path('permissiondenied/',notEnoughPerm,name='permissiondenied'),
    path('clockedIn/',clockedIn,name='clockedIn')
    # path('w/', homepage2,name='home-main2'),
]
