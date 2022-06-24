from django.contrib import admin
from django.urls import path, include
from .views import api_call


urlpatterns = [
    path('<slug:endpoint>', api_call, name='api'),
]
