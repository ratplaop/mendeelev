from django.db import models
from django.contrib.auth.models import User

class Events(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.event_name
