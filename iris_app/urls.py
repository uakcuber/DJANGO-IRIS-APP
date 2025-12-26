from django.urls import path, include
from django.contrib.auth import views as auth_views  # <-- BU SATIR ÇOK ÖNEMLİ
from rest_framework.routers import DefaultRouter
from . import views

# API Router ayarı (Bonus Puan İçin)
router = DefaultRouter()
router.register(r'api/plants', views.IrisPlantViewSet)

urlpatterns = [
    # Mevcut Sayfalar
    path('', views.plant_list, name='plant_list'),
    path('add/', views.plant_create, name='plant_create'),
    path('update/<int:pk>/', views.plant_update, name='plant_update'),
    path('delete/<int:pk>/', views.plant_delete, name='plant_delete'),
    path('search/', views.plant_search, name='plant_search'),
    path('import-export/', views.data_import_export, name='data_import_export'),

    # Kimlik Doğrulama (Login/Logout/Register)
    path('register/', views.register, name='register'),

    # HATA VEREN KISIM DÜZELTİLDİ:
    # Artık views.auth_views değil, direkt auth_views kullanıyoruz.
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('predict/', views.predict_species, name='predict_species'),

    # BONUS API URL'i:
    path('', include(router.urls)),
]