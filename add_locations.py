import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from iris_app.models import Location

# Örnek konumlar
locations_data = [
    {'city': 'İstanbul', 'region': 'Marmara', 'altitude': 50},
    {'city': 'Ankara', 'region': 'İç Anadolu', 'altitude': 890},
    {'city': 'İzmir', 'region': 'Ege', 'altitude': 24},
    {'city': 'Antalya', 'region': 'Akdeniz', 'altitude': 57},
    {'city': 'Bursa', 'region': 'Marmara', 'altitude': 95},
    {'city': 'Gaziantep', 'region': 'Güneydoğu Anadolu', 'altitude': 919},
]

for loc in locations_data:
    location, created = Location.objects.get_or_create(
        city=loc['city'],
        defaults={
            'region': loc['region'],
            'altitude': loc['altitude']
        }
    )
    if created:
        print(f"✅ Eklendi: {location.city}")
    else:
        print(f"⚠️  Zaten var: {location.city}")

print("\n✅ Tamamlandı!")
