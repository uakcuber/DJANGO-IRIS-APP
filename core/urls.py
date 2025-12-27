# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('iris_app.urls')),# Anasayfa direkt iris_app'e gitsin
]
