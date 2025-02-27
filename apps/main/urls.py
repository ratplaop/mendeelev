from django.urls import path
from . import views
from .views import NewsView, EventDetailView, NewsDetailView  # Убедитесь, что вы импортировали ваши представления

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),  # URL для новостей
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),  # URL для деталей мероприятия
  
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # URL для дет # URL для деталей новости
]
