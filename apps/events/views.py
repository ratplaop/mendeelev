from django.views.generic import ListView
from .models import Events

class EventsListView(ListView):
    model = Events
    template_name = 'events/list.html'
    context_object_name = 'objects'

class IndexView(ListView):
    model = Events
    template_name = 'events/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Events.objects.all()
