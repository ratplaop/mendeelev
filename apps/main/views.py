from django.views.generic import ListView, TemplateView, DetailView
from .models import Main, Event, News, MainNews
from django.shortcuts import render

class MainListView(ListView):
    model = Main
    template_name = 'main/list.html'
    context_object_name = 'objects'

class IndexView(ListView):
    model = Main
    template_name = 'main/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Main.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.all()
        context['event_list'] = Event.objects.all()
        return context

class NewsView(TemplateView):
    template_name = 'main/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.all()
        context['event_list'] = Event.objects.all()
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'main/event_detail.html'
    context_object_name = 'event'

class NewsDetailView(DetailView):
    model = News
    template_name = 'main/news_detail.html'
    context_object_name = 'news_item'

def news_list(request):
    news = MainNews.objects.all()  # Получаем все новости
    return render(request, 'news/news_list.html', {'news': news})
