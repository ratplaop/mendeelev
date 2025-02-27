from django.db import models
from django.contrib.auth.models import User

class Regions(models.Model):
    region_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.region_name
