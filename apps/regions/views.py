from django.views.generic import ListView
from .models import Regions

class RegionsListView(ListView):
    model = Regions
    template_name = 'regions/list.html'
    context_object_name = 'objects'

class IndexView(ListView):
    model = Regions
    template_name = 'regions/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Regions.objects.all()
