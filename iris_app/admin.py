from django.contrib import admin
from .models import IrisPlant, Location

# Modelleri admin panelinde görünür yapıyoruz
admin.site.register(IrisPlant)
admin.site.register(Location)