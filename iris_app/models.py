from django.db import models

# MODEL TANIMLARI BURADA
class Location(models.Model):
    city = models.CharField(max_length=100, verbose_name="Şehir")
    # Region ve Altitude alanlarını eklemişsin, gayet güzel
    region = models.CharField(max_length=100, verbose_name="Bölge", blank=True, null=True)
    altitude = models.IntegerField(verbose_name="Rakım (m)", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Admin panelinde ve formda görünecek isim
        if self.region:
            return f"{self.city} ({self.region})"
        return self.city



class IrisPlant(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='plants', verbose_name="Konum",
                                 null=True, blank=True)

    # Dataset Sütunları
    sepal_length = models.FloatField(verbose_name="Sepal Length (cm)")
    sepal_width = models.FloatField(verbose_name="Sepal Width (cm)")
    petal_length = models.FloatField(verbose_name="Petal Length (cm)")
    petal_width = models.FloatField(verbose_name="Petal Width (cm)")

    species = models.CharField(max_length=50, verbose_name="Tür")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.species} - {self.pk}"