from django.views.generic import ListView
from .models import TelegramBot

class Telegram_botListView(ListView):
    model = TelegramBot
    template_name = 'telegram_bot/list.html'
    context_object_name = 'objects'

class IndexView(ListView):
    model = TelegramBot
    template_name = 'telegram_bot/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return TelegramBot.objects.all()
