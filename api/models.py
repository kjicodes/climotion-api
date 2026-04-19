from django.db import models

class SearchedCity(models.Model):
    city_name = models.CharField(max_length=100, blank=False)
    class Meta:
        verbose_name = "Searched City"
        verbose_name_plural = "Searched Cities"

    def __str__(self):
        return self.city_name
