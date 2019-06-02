from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from titanic import views

router = routers.DefaultRouter() 
router.register(r'titanic', views.TitanicViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
