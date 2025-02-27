from django.urls import path
from . import views

app_name = 'telegram_bot'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
