from django.db import models
from django.contrib.auth.models import User

class TelegramBot(models.Model):
    bot_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Телеграм бот"
        verbose_name_plural = "Телеграм боты"

    def __str__(self):
        return self.bot_name
