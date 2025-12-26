# core/urls.py
from django.contrib import admin
from django.urls import path, include  # include'u eklemeyi unutma!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('iris_app.urls')),  # Burayı ekle: Anasayfa direkt iris_app'e gitsin
]
