from django.views.generic import ListView
from .models import News

class NewsListView(ListView):
    model = News
    template_name = 'news/list.html'
    context_object_name = 'objects'

class IndexView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return News.objects.all()
